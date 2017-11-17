# -*- coding: utf-8 -*-
import os.path

from .paths import PROJECT_DIR

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'fnpdjango.utils.pipeline_storage.GzipPipelineCachedStorage'
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
          'css/base.scss',
          'css/main.scss',
          'css/form.scss',
          'catalogue/css/layout.scss',
          'catalogue/css/exercise.scss',
          'jquery/colorbox/colorbox.css',
          'fnpdjango/annoy/annoy.css',
        ),
        'output_filename': 'compressed/base.css',
    },
}
PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'jquery/colorbox/jquery.colorbox-min.js',
            'jquery/colorbox/jquery.colorbox-pl.js',
            'catalogue/js/edumed.js',
            'sponsors/js/sponsors.js',
            'js/formset.js',
            'fnpdjango/annoy/annoy.js',
            'js/checkfile.js',
        ),
        'output_filename': 'compressed/base.js',
    },
    'wtem': {
        'source_filenames': (
            'js/jquery-ui-1.10.0.custom.js',
            'wtem/edumed.js',
            'wtem/wtem.js',
            'wtem/json2.js'
        ),
        'output_filename': 'compressed/wtem.js'
    },
}

PIPELINE_COMPILERS = (
  'pipeline.compilers.sass.SASSCompiler',
)
