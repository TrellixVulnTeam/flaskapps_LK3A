from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..db import models, schemas
from ..utils import *
from ..utils import check_updates as _update_check
from docker.errors import APIError

from datetime import datetime
import time
import subprocess
import docker


def get_running_apps():
    apps_list = []
    dclient = docker.from_env()
    apps = dclient.containers.list()
    for app in apps:
        attrs = app.attrs
        attrs.update(conv2dict("name", app.name))
        attrs.update(conv2dict("ports", app.ports))
        attrs.update(conv2dict("short_id", app.short_id))
        apps_list.append(attrs)

    return apps_list


def check_app_update(app_name):
    dclient = docker.from_env()
    try:
        app = dclient.containers.get(app_name)
    except Exception as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )

    if app.attrs["Config"]["Image"]:
        if _update_check(app.attrs["Config"]["Image"]):
            app.attrs.update(conv2dict("isUpdatable", True))
    app.attrs.update(conv2dict("name", app.name))
    app.attrs.update(conv2dict("ports", app.ports))
    app.attrs.update(conv2dict("short_id", app.short_id))
    return app.attrs


def get_apps():
    apps_list = []
    dclient = docker.from_env()
    try:
        apps = dclient.containers.list(all=True)
    except Exception as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )
    for app in apps:
        attrs = app.attrs

        attrs.update(conv2dict("name", app.name))
        attrs.update(conv2dict("ports", app.ports))
        attrs.update(conv2dict("short_id", app.short_id))
        apps_list.append(attrs)

    return apps_list


def get_app(app_name):
    dclient = docker.from_env()
    try:
        app = dclient.containers.get(app_name)
    except Exception as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )
    attrs = app.attrs

    attrs.update(conv2dict("ports", app.ports))
    attrs.update(conv2dict("short_id", app.short_id))
    attrs.update(conv2dict("name", app.name))

    return attrs


def get_app_processes(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    if app.status == "running":
        processes = app.top()
        return schemas.Processes(
            Processes=processes["Processes"], Titles=processes["Titles"]
        )
    else:
        return None


def get_app_logs(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    if app.status == "running":
        return schemas.AppLogs(logs=app.logs())
    else:
        return None


def deploy_app(template: schemas.DeployForm):
    try:
        launch = launch_app(
            template.name,
            conv_image2data(template.image),
            conv_restart2data(template.restart_policy),
            conv_ports2data(template.ports, template.network, template.network_mode),
            conv_portlabels2data(template.ports),
            template.network_mode,
            template.network,
            conv_volumes2data(template.volumes),
            conv_env2data(template.env),
            conv_devices2data(template.devices),
            conv_labels2data(template.labels),
            conv_sysctls2data(template.sysctls),
            conv_caps2data(template.cap_add),
        )
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    except Exception as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )
    print("done deploying")

    return schemas.DeployLogs(logs=launch.logs())


def Merge(dict1, dict2):
    if dict1 and dict2:
        return dict2.update(dict1)
    elif dict1:
        return dict1
    elif dict2:
        return dict2
    else:
        return None


def launch_app(
    name,
    image,
    restart_policy,
    ports,
    portlabels,
    network_mode,
    network,
    volumes,
    env,
    devices,
    labels,
    sysctls,
    caps,
):
    dclient = docker.from_env()
    combined_labels = Merge(portlabels, labels)
    try:
        lauch = dclient.containers.run(
            name=name,
            image=image,
            restart_policy=restart_policy,
            ports=ports,
            network=network,
            network_mode=network_mode,
            volumes=volumes,
            environment=env,
            sysctls=sysctls,
            labels=combined_labels,
            devices=devices,
            cap_add=caps,
            detach=True,
        )
    except Exception as e:
        if e.status_code == 500:
            failed_app = dclient.containers.get(name)
            failed_app.remove()
        raise e

    print(
        f"""Container started successfully.
       Name: {name},
      Image: {image},
      Ports: {ports},
    Volumes: {volumes},
        Env: {env}"""
    )
    return lauch


def app_action(app_name, action):
    err = None
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    _action = getattr(app, action)
    if action == "remove":
        try:
            _action(force=True)
        except Exception as exc:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )
    else:
        try:
            _action()
        except Exception as exc:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )
    apps_list = get_apps()
    return apps_list


def app_update(app_name):
    dclient = docker.from_env()
    try:
        old = dclient.containers.get(app_name)
    except Exception as exc:
        print(exc)
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Unable to get container ID",
            )
        else:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )

    volumes = {"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}}
    try:
        updater = dclient.containers.run(
            image="containrrr/watchtower:latest",
            command="--cleanup --run-once " + old.name,
            remove=True,
            detach=True,
            volumes=volumes,
        )
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.explanation
        )

    print("**** Updating " + old.name + "****")
    result = updater.wait(timeout=120)
    print(result)
    time.sleep(1)
    return get_apps()


def update_self():
    dclient = docker.from_env()
    bash_command = "head -1 /proc/self/cgroup|cut -d/ -f3"
    yacht_id = (
        subprocess.check_output(["bash", "-c", bash_command]).decode("UTF-8").strip()
    )
    try:
        yacht = dclient.containers.get(yacht_id)
    except Exception as exc:
        print(exc)
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Unable to get Yacht container ID",
            )
        else:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )

    volumes = {"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}}
    print("**** Updating " + yacht.name + "****")
    updater = dclient.containers.run(
        image="containrrr/watchtower:latest",
        command="--cleanup --run-once " + yacht.name,
        remove=True,
        detach=True,
        volumes=volumes,
    )
    result = updater
    print(result)
    time.sleep(1)
    return result


def check_self_update():
    dclient = docker.from_env()
    bash_command = "head -1 /proc/self/cgroup|cut -d/ -f3"
    yacht_id = (
        subprocess.check_output(["bash", "-c", bash_command]).decode("UTF-8").strip()
    )
    try:
        yacht = dclient.containers.get(yacht_id)
    except Exception as exc:
        print(exc)
        if hasattr(exc, 'response') and exc.response.status_code == 404:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Unable to get Yacht container ID",
            )
        elif hasattr(exc, 'response'):
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.explanation
            )
        else:
            raise HTTPException(
                status_code=400, detail=exc.args
            )

    return _update_check(yacht.image.tags[0])
