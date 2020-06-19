
def MAVEN_CONTAINER = "registry.redhat.io/openshift3/jenkins-agent-maven-35-rhel7:v3.11"
def CONTAINER_NAME = 'jnlp'
def JVM_OPTIONS = "-DproxySet=true -DproxyHost=vsdbahlprxy1 -DproxyPort=8080"

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
    serviceAccount: 'jenkins',
    /*
       Add a Config Map example
       volumes: [ configMapVolume(configMapName: "mvn-settings", mountPath: "/cfg")],
     */
    containers: [
      containerTemplate(name: CONTAINER_NAME,
                        image: MAVEN_CONTAINER,
                        envVars: [envVar(key: 'PATH', value: '/opt/rh/rh-maven35/root/usr/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin')] )]
    ) {
      node(BUILD_TAG) {

        stage('Clone Repository'){
          checkout scm
        }

        container(CONTAINER_NAME) {
          stage('Creating Openshift Objects') {
            sh "python create.py project=${PROJECT} name=${APPLICATION_NAME}"
          }

          stage("Compile and Testing"){
            sh "mvn ${JVM_OPTIONS} test package"
          }

          stage('Creating Container'){
            sh "oc start-build bc/${APPLICATION_NAME} --from-file=\$(ls target/*.jar) --follow"
            //sh "oc wait dc/${APPLICATION_NAME} --for condition=available --timeout=-1s"
          }

        }

      }
}
