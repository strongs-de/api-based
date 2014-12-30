module.exports = (grunt) ->
    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        coffee:
            files:
                src: ['strongs/src/js/**/*.coffee']
                dest: 'strongs/assets/js/script.js'
        watch:
            src:
                files: [
                    'strongs/src/**/*.coffee',
                    'strongs/src/**/*.less'
                ],
                tasks: ['coffee', 'less', 'copy']
        less:
            options:
                paths: ['strongs/src/css']
            files:
                dest: 'strongs/assets/css/style.css',
                src: ['strongs/src/less/**/*.less']
        copy:
            main:
                files: [
                    {
                        expand: true,
                        cwd: 'strongs/fonts',
                        src: '**',
                        dest: 'strongs/assets/fonts',
                        flatten: true
                    },
                    {
                        expand: true,
                        cwd: 'strongs/media',
                        src: '**',
                        dest: 'strongs/assets/media',
                        flatten: true
                    },
                    {
                        expand: true,
                        cwd: 'strongs/src/elements',
                        src: '**',
                        dest: 'strongs/assets/elements',
                        flatten: true
                    }
                ]
    )

    grunt.loadNpmTasks('grunt-contrib-coffee')
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');

    grunt.registerTask('default', ['coffee', 'less', 'copy', 'watch'])
