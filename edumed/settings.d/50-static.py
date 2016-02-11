MEDIA_ROOT = path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
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
          'catalogue/css/carousel.scss',
          'catalogue/css/layout.scss',
          'catalogue/css/lesson.scss',
          'catalogue/css/exercise.scss',
          'catalogue/css/section_list.scss',
          'curriculum/curriculum.scss',
          'jquery/colorbox/colorbox.css',
          'fnpdjango/annoy/annoy.css',

          'css/forum.scss',
          'css/mil.scss'
        ),
        'output_filename': 'compressed/base.css',
    },
}
PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'catalogue/js/jquery-ui-1.10.0.custom.js',
            'catalogue/js/jquery.cycle.all.js',
            'jquery/colorbox/jquery.colorbox-min.js',
            'jquery/colorbox/jquery.colorbox-pl.js',
            'catalogue/js/carousel.js',
            'catalogue/js/edumed.js',
            'catalogue/js/lesson.js',
            'catalogue/js/lesson-list.js',
            'sponsors/js/sponsors.js',
            'curriculum/curriculum.js',
            'js/formset.js',
            'pybb/js/pybbjs.js',
            'fnpdjango/annoy/annoy.js',
        ),
        'output_filename': 'compressed/base.js',
    },
    'wtem': {
        'source_filenames': (
            'catalogue/js/jquery-ui-1.10.0.custom.js',
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
