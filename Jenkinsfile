pipeline {
  agent any

  environment {
    // INTERNAL (LAN) registry used for build/push
    REGISTRY_INTERNAL   = '10.172.27.13:3000'
    OWNER               = 'nidhun'
    IMAGE_NAME          = 'django-crm'
    DOCKER_REPO_INTERNAL= "${REGISTRY_INTERNAL}/${OWNER}/${IMAGE_NAME}"

    // Public hostname only for display/pulls
    REGISTRY_PUBLIC     = 'gitea.nidhun.me'
    DOCKER_REPO_PUBLIC  = "${REGISTRY_PUBLIC}/${OWNER}/${IMAGE_NAME}"

    DOCKER_CREDENTIALS_ID = 'gitea-docker-registry'
  }

  stages {
    stage('Checkout & Submodule') {
      steps {
        checkout scm
        sh 'git submodule update --init --recursive'
        script {
          env.GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          env.BUILD_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
        }
      }
    }

    stage('Build Optimized Image') {
      steps {
        sh """
          echo "🏗️ Building ${DOCKER_REPO_INTERNAL}:${BUILD_TAG}"
          docker build -t ${DOCKER_REPO_INTERNAL}:${BUILD_TAG} .
          docker tag  ${DOCKER_REPO_INTERNAL}:${BUILD_TAG} ${DOCKER_REPO_INTERNAL}:latest

          echo "📊 Image size:"
          docker images | grep ${IMAGE_NAME} || true
        """
      }
    }

    stage('Push (Internal LAN Registry)') {
      steps {
        withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID,
                                          usernameVariable: 'USER',
                                          passwordVariable: 'PASS')]) {
          // generous timeout in case layers are big
          timeout(time: 30, unit: 'MINUTES') {
            sh """
              echo "🔐 Login to internal registry..."
              echo "\$PASS" | docker login ${REGISTRY_INTERNAL} -u "\$USER" --password-stdin

              echo "📡 Checking registry API..."
              curl -sI http://${REGISTRY_INTERNAL}/v2/ | head -n1

              echo "🚀 Pushing image tag: ${BUILD_TAG}"
              docker push ${DOCKER_REPO_INTERNAL}:${BUILD_TAG}

              echo "🚀 Pushing latest"
              docker push ${DOCKER_REPO_INTERNAL}:latest

              echo "✅ Push complete (internal)"
            """
          }
        }
      }
    }
  }

  post {
    success {
      echo "✅ Done! Pulled URL (public): ${DOCKER_REPO_PUBLIC}:${BUILD_TAG}"
    }
    always {
      // optional: avoid storing creds
      sh "docker logout ${REGISTRY_INTERNAL} || true"

      // clean only our images
      sh """
        docker rmi ${DOCKER_REPO_INTERNAL}:${BUILD_TAG}  || true
        docker rmi ${DOCKER_REPO_INTERNAL}:latest       || true
      """
    }
  }
}
