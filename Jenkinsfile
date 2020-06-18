
def MAVEN_CONTAINER = "registry.redhat.io/openshift3/jenkins-agent-maven-35-rhel7:v3.11"
def JNLP_CONTAINER = 'jnlp'

/*
  Jenkins variables from the install.yml:
  APPLICATION_NAME

*/

/*
   This creates a container to run your build, as you can see using the default
   agent has its limitations.

   For more info: https://cesarvr.io/post/jenkins-container/
 */

podTemplate(
    cloud:'openshift',
    label: BUILD_TAG,
    /*
       Add a Config Map example
       volumes: [ configMapVolume(configMapName: "mvn-settings", mountPath: "/cfg")],
     */
    containers: [ containerTemplate(name: "jnlp", image: MAVEN_CONTAINER) ] ) {
  node(BUILD_TAG) {

    stage('Clone Repository'){
      checkout scm
    }

    container(JNLP_CONTAINER) {
      stage('Creating Openshift Objects') {
        sh "ls -art"
        sh "python deploy.py project=${PROJECT} name=${APPLICATION_NAME}"
      }

      stage("Compile and Testing"){
        sh "mvn test package"
      }

      stage('Creating Container'){
        sh "oc start-build bc/${APPLICATION_NAME} --from-file=\$(ls target/*.jar) --follow"
      }

    }

  }
}
