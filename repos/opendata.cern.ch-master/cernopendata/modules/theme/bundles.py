# -*- coding: utf-8 -*-
#
# This file is part of CERN Open Data Portal.
# Copyright (C) 2017 CERN.
#
# CERN Open Data Portal is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Open Data Portal is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Open Data Portal; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""JS/CSS bundles for theme."""

from __future__ import absolute_import, print_function

from flask_assets import Bundle
from invenio_assets import NpmBundle

visualise_js = NpmBundle(
    'node_modules/d3/d3.min.js',
    'node_modules/flot/jquery.flot.js',
    'node_modules/flot/jquery.flot.selection.js',
    'js/visualise/visualise_histograms.js',
    output='gen/cernopendata.%(version)s.js',
    npm={
        'd3': '^3.3.13',
        'flot': '~0.8.0-alpha',
    },
)

visualise_css = NpmBundle(
    'scss/visualise.scss',
    filters='node-scss, cleancss',
    output='gen/cernopendata.vis.%(version)s.css',
    npm={
        "bootstrap-sass": "~3.3.5",
    }
)

glossary_js = NpmBundle(
    'js/glossary/jquery.zglossary.js',
    output='gen/glossary.%(version)s.js',
    npm={},
)

glossary_css = NpmBundle(
    'js/glossary/jquery.zglossary.css',
    filters='node-scss, cleancss',
    output='gen/cernopendata.glossary.%(version)s.css',
    npm={
        "bootstrap-sass": "~3.3.5",
    }
)

ispy_js = NpmBundle(
    # "node_modules/ispy-webgl/js/lib/jquery-1.11.1.min.js",
    "node_modules/ispy-webgl/js/lib/jquery.scrollintoview.min.js",
    "node_modules/ispy-webgl/js/lib/stupidtable.min.js",
    # 'node_modules/bootstrap/dist/js/bootstrap.js',
    # "node_modules/ispy-webgl/js/lib/bootstrap.min.js",
    "node_modules/ispy-webgl/js/lib/stats.min.js",
    "node_modules/ispy-webgl/js/lib/three.min.js",
    "node_modules/ispy-webgl/js/lib/tween.min.js",
    "node_modules/ispy-webgl/js/lib/CombinedCamera.js",
    "node_modules/ispy-webgl/js/lib/TrackballControls.js",
    "node_modules/ispy-webgl/js/lib/Projector.js",
    "node_modules/ispy-webgl/js/lib/CanvasRenderer.js",
    "node_modules/ispy-webgl/js/lib/SVGRenderer.js",
    "node_modules/ispy-webgl/js/lib/MTLLoader.js",
    "node_modules/ispy-webgl/js/lib/OBJLoader.js",
    "node_modules/ispy-webgl/js/lib/OBJExporter.js",
    "node_modules/ispy-webgl/js/lib/STLExporter.js",
    "node_modules/ispy-webgl/js/lib/GLTFExporter.js",
    "node_modules/ispy-webgl/js/lib/jszip.min.js",
    "node_modules/ispy-webgl/js/lib/DeviceOrientationControls.js",
    "node_modules/ispy-webgl/js/lib/StereoEffect.js",
    "node_modules/ispy-webgl/js/lib/StereoCamera.js",
    "node_modules/ispy-webgl/js/config.js",
    "node_modules/ispy-webgl/js/setup.js",
    "node_modules/ispy-webgl/js/animate.js",
    "node_modules/ispy-webgl/js/files-load.js",
    "node_modules/ispy-webgl/js/objects-draw.js",
    "node_modules/ispy-webgl/js/objects-add.js",
    "node_modules/ispy-webgl/js/objects-config.js",
    # <!-- These geometries are loaded regardless of the renderer used -->
    "node_modules/ispy-webgl/geometry/dt.js",
    "node_modules/ispy-webgl/geometry/csc.js",
    "node_modules/ispy-webgl/geometry/rpc.js",
    # <!-- Don't load this anymore as we don't use the models for WebGL
    # "node_modules/ispy-webgl/geometry/ecal.js",
    "node_modules/ispy-webgl/js/controls.js",
    "node_modules/ispy-webgl/js/tree-view.js",
    "node_modules/ispy-webgl/js/display.js",
    "node_modules/ispy-webgl/js/ispy.js",
    output='gen/cernopendata.ispy.%(version)s.js',
    npm={
        "ispy-webgl": "0.9.8-COD3.11"
    },
)

ispy_css = NpmBundle(
    "node_modules/ispy-webgl/css/font-awesome.min.css",
    "node_modules/ispy-webgl/css/ispy.css",
    filters='node-scss, cleancss',
    output='gen/cernopendata.ispy.%(version)s.css',
    npm={
        "ispy-webgl": "0.9.8-COD3.11"
    }
)


codemirror_js = NpmBundle(
    'node_modules/codemirror/lib/codemirror.js',
    'node_modules/codemirror/mode/scheme/scheme.js',
    'node_modules/codemirror/mode/javascript/javascript.js',
    'node_modules/codemirror/mode/xml/xml.js',
    # 'node_modules/angular-ui-codemirror/src/ui-codemirror.js',
    # 'node_modules/angular-clipboard/angular-clipboard.js',
    output='gen/cernopendata.codemirror.%(version)s.js',
    npm={
        # "angular-ui-codemirror": "0.3.0",
        "codemirror": "*",
        # "angular-clipboard": "1.6.2",
    },
)

codemirror_css = NpmBundle(
    Bundle(
        'node_modules/codemirror/lib/codemirror.css',
        filters='cleancssurl',
    ),
    depends=('scss/*.scss',),
    output='gen/cernopendata.codemirror.%(version)s.css',
    npm={
    }
)
