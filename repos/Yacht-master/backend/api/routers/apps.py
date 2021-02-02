from fastapi import APIRouter, Depends, HTTPException, WebSocket, status, Cookie
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import make_transient

from ..db import models, schemas
from ..db.models import containers
from ..db.database import SessionLocal, engine
from .. import actions
from ..auth import get_active_user, User
from ..utils import (
    websocket_auth,
    calculate_blkio_bytes,
    calculate_cpu_percent,
    calculate_cpu_percent2,
    calculate_network_bytes,
    get_app_stats,
)

import docker as sdocker
import aiodocker
from datetime import datetime
import urllib.request
import json
import asyncio

containers.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", dependencies=[Depends(get_active_user)])
def index():
    return actions.get_apps()


@router.get("/{app_name}/updates", dependencies=[Depends(get_active_user)])
def check_app_updates(app_name):
    return actions.check_app_update(app_name)


@router.get("/{app_name}/update", dependencies=[Depends(get_active_user)])
def update_container(app_name):
    return actions.app_update(app_name)


@router.get("/{app_name}", dependencies=[Depends(get_active_user)])
def get_container_details(app_name):
    return actions.get_app(app_name=app_name)


@router.get(
    "/{app_name}/processes",
    response_model=schemas.Processes,
    dependencies=[Depends(get_active_user)],
)
def get_container_processes(app_name):
    return actions.get_app_processes(app_name=app_name)


@router.get(
    "/{app_name}/logs",
    response_model=schemas.AppLogs,
    dependencies=[Depends(get_active_user)],
)
def get_container_logs(app_name):
    return actions.get_app_logs(app_name=app_name)


@router.get("/actions/{app_name}/{action}", dependencies=[Depends(get_active_user)])
def container_actions(app_name, action):
    return actions.app_action(app_name, action)


@router.post(
    "/deploy",
    response_model=schemas.DeployLogs,
    dependencies=[Depends(get_active_user)],
)
def deploy_app(template: schemas.DeployForm):
    return actions.deploy_app(template=template)


@router.websocket("/{app_name}/livelogs")
async def logs(websocket: WebSocket, app_name: str):

    auth_success = await websocket_auth(websocket=websocket)
    if auth_success:
        await websocket.accept()
        async with aiodocker.Docker() as docker:
            container: DockerContainer = await docker.containers.get(app_name)
            if container._container["State"]["Status"] == "running":
                stats = container.stats(stream=True)
                logs = container.log(stdout=True, stderr=True, follow=True)
                async for line in logs:
                    try:
                        await websocket.send_text(line)
                    except Exception as e:
                        return e
            else:
                await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)


@router.websocket("/{app_name}/stats")
async def stats(websocket: WebSocket, app_name: str):

    auth_success = await websocket_auth(websocket=websocket)
    if auth_success:
        await websocket.accept()
        async with aiodocker.Docker() as docker:
            cpu_total = 0.0
            cpu_system = 0.0
            cpu_percent = 0.0

            container: DockerContainer = await docker.containers.get(app_name)
            if container._container["State"]["Status"] == "running":
                stats = container.stats(stream=True)

                async for line in stats:
                    if line["memory_stats"]:
                        mem_current = line["memory_stats"]["usage"]
                        mem_total = line["memory_stats"]["limit"]
                        mem_percent = (mem_current / mem_total) * 100.0
                    else:
                        mem_current = None
                        mem_total = None
                        mem_percent = None

                    try:
                        (
                            cpu_percent,
                            cpu_system,
                            cpu_total,
                        ) = await calculate_cpu_percent2(line, cpu_total, cpu_system)
                    except KeyError as e:
                        print("error while getting new CPU stats: %r, falling back")
                        cpu_percent = await calculate_cpu_percent(line)

                    full_stats = {
                        "time": line["read"],
                        "cpu_percent": cpu_percent,
                        "mem_current": mem_current,
                        "mem_total": mem_total,
                        "mem_percent": mem_percent,
                    }
                    try:
                        await websocket.send_text(json.dumps(full_stats))
                    except Exception as e:
                        return e
            else:
                await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)


@router.websocket("/stats")
async def dashboard(websocket: WebSocket):
    auth_success = await websocket_auth(websocket=websocket)
    if auth_success:
        await websocket.accept()
        tasks = []
        async with aiodocker.Docker() as docker:
            containers = []
            _containers = await docker.containers.list()
            for _app in _containers:
                if _app._container["State"] == "running":
                    containers.append(_app)
            for app in containers:
                _name = app._container["Names"][0][1:]
                container: DockerContainer = await docker.containers.get(_name)
                stats = container.stats(stream=True)
                tasks.append(process_container(_name, stats, websocket))
            await asyncio.gather(*tasks)
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)


async def process_container(name, stats, websocket):
    cpu_total = 0.0
    cpu_system = 0.0
    cpu_percent = 0.0
    async for line in stats:
        if line["memory_stats"]:
            mem_current = line["memory_stats"]["usage"]
            mem_total = line["memory_stats"]["limit"]
            mem_percent = (mem_current / mem_total) * 100.0
        else:
            mem_current = None
            mem_total = None
            mem_percent = None

        try:
            cpu_percent, cpu_system, cpu_total = await calculate_cpu_percent2(
                line, cpu_total, cpu_system
            )
        except KeyError as e:
            print("error while getting new CPU stats: %r, falling back")
            cpu_percent = await calculate_cpu_percent(line)

        full_stats = {
            "name": name,
            "cpu_percent": cpu_percent,
            "mem_current": mem_current,
            "mem_total": mem_total,
            "mem_percent": mem_percent,
        }
        try:
            await websocket.send_text(json.dumps(full_stats))
        except Exception as e:
            pass
