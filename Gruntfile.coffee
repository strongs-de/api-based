module.exports = (grunt) ->
    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        coffee:
            files:
                src: ['strongs/src/js/**/*.coffee']
                dest: 'strongs/assets/js/script.js'
        watch: {
            src: {
                files: ['strongs/src/js/**/*.coffee'],
                tasks: []
            }
        }
    )

    grunt.loadNpmTasks('grunt-contrib-coffee')
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['coffee', 'watch'])
