// Jenkins pipeline that builds the Django CRM Docker image and pushes it to
// the Gitea container registry.
pipeline {
  // Run on any available Jenkins agent (it needs Docker and git installed)
  agent any

  environment {
    // INTERNAL (LAN) registry used for build/push
    REGISTRY_INTERNAL   = '10.172.27.13:3000'
    // Registry owner (Gitea user or organisation) and image name
    OWNER               = 'nidhun'
    IMAGE_NAME          = 'django-crm'
    // Full image name on the internal registry
    DOCKER_REPO_INTERNAL= "${REGISTRY_INTERNAL}/${OWNER}/${IMAGE_NAME}"

    // Public hostname only for display/pulls
    REGISTRY_PUBLIC     = 'gitea.nidhun.me'
    DOCKER_REPO_PUBLIC  = "${REGISTRY_PUBLIC}/${OWNER}/${IMAGE_NAME}"

    // ID of the Jenkins username/password credential for the registry
    DOCKER_CREDENTIALS_ID = 'gitea-docker-registry'
  }

  stages {
    // Get the code, including the django-crm submodule, and work out the tag
    stage('Checkout & Submodule') {
      steps {
        checkout scm
        sh 'git submodule update --init --recursive'
        script {
          // Tag images as <build number>-<short commit hash>, e.g. 12-a1b2c3d
          env.GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          env.BUILD_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
        }
      }
    }

    // Build the image from the Dockerfile and also tag it as latest
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

    // Log in to the registry and push both tags
    stage('Push (Internal LAN Registry)') {
      steps {
        // Load the registry username and password into USER and PASS
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

  // Steps that run after all stages
  post {
    // On success, print the public image name to pull
    success {
      echo "✅ Done! Pulled URL (public): ${DOCKER_REPO_PUBLIC}:${BUILD_TAG}"
    }
    // Always clean up, whether the build passed or failed
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
