module.exports = (grunt) ->
    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        coffee:
            files:
                src: ['strongs/src/js/**/*.coffee']
                dest: 'strongs/assets/js/script.js'
        watch: {
            src:
                files: [
                    'strongs/src/js/**/*.coffee',
                    'strongs/src/css/**/*.less'
                ],
                tasks: ['coffee', 'less']
        }
        less: {
            options:
                paths: ['strongs/src/css']
            files:
                dest: 'strongs/assets/css/style.css',
                src: ['strongs/src/css/**/*.less']
        }
    )

    grunt.loadNpmTasks('grunt-contrib-coffee')
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');

    grunt.registerTask('default', ['coffee', 'less', 'watch'])
