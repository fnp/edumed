MEDIA_ROOT = path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
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

          'css/annoy.css',
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
            'catalogue/js/edumed.js',
            'catalogue/js/lesson.js',
            'sponsors/js/sponsors.js',
            'curriculum/curriculum.js',

            'js/annoy.js',
        ),
        'output_filename': 'compressed/base.js',
    },
}

PIPELINE_COMPILERS = (
  'pipeline.compilers.sass.SASSCompiler',
)

PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'
