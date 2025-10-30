import java.text.SimpleDateFormat

import hudson.model.*
import jenkins.model.*

def currentDate = new Date()
String currentTimeFormat = currentDate.format("yyyy-MM-dd")

def dockerComposeDown(remoteServer) {
	echo "docker compose down on ${remoteServer}"
	sh "ssh ${sshOptions} ${sshUser}@${remoteServer} 'cd ${dockerComposeHome}/${repositoryName}; docker compose down'"
}

def dockerComposeBuild(remoteServer) {
	echo "docker compose build on ${remoteServer}"
	sh "ssh ${sshOptions} ${sshUser}@${remoteServer} 'cd ${dockerComposeHome}/${repositoryName}; docker compose build'"
}

def dockerComposeUp(remoteServer) {
	echo "docker compose up on ${remoteServer}"
	sh "ssh ${sshOptions} ${sshUser}@${remoteServer} 'cd ${dockerComposeHome}/${repositoryName}; docker compose up'"
}

def dockerComposeBuildUp(remoteServer) {
	echo "docker compose up on ${remoteServer}"
	sh "ssh ${sshOptions} ${sshUser}@${remoteServer} 'cd ${dockerComposeHome}/${repositoryName}; docker compose down && docker compose up --build'"
}

def gitPullRepo() {
	echo "Pull ${repositoryName} from ${repositoryURL}"
	sh "\
		test -d ${repositoryName} && rm -rf ${repositoryName}/; \
		git clone -q ${repositoryURL}; \
	"
}

def copyRepo(remoteServer) {
	echo "Copy repo to ${remoteServer}"
	sh "rsync -aAXHPv --exclude .git --exclude .gitignore --exclude .gitlab-ci.yml --exclude ansible/ --delete-after ${WORKSPACE}/${repositoryName} ${remoteServer}:${dockerComposeHome}/"
}

pipeline {
	agent {
		label "jenkins-reserved"
	}
	environment {
		jenkinsUrl = "https://jenkins-blueocean.mja.io"
		buildLogBlue = "${jenkinsUrl}/blue/organizations/jenkins/${env.JOB_BASE_NAME}/detail/${env.JOB_BASE_NAME}/${BUILD_NUMBER}/pipeline"
		toMail = "sergey.gurovich@gmail.com"
		fromMail = "jenkins@jenkins-blueocean.mja.io"

		sshUser = "jenkins"
		dockerComposeHome = "/home/${sshUser}"
		repositoryName = "weather_report"
		repositoryURL = "git@github.com:sgplay/${repositoryName}.git"
		abortTimer = "30"      // Abort pipeline after timeout (sec) if no user input
		sshOptions = ' ' //'-o UserKnownHostsFile=/dev/null,StrictHostKeyChecking=no'
	}

	parameters {
		choice(name: 'operationType', choices: ['dockerComposeBuildUp', 'dockerComposeDown', 'dockerComposeBuild', 'dockerComposeUp'], description: 'Select operation')
		string(name: 'remoteServer', description: 'Target machine IP to build and run the project:', defaultValue: '192.168.1.5')
	}
	
	stages {
		stage('defineVars') {
			steps {
				sh 'cd ${WORKSPACE}'
				wrap([$class: 'BuildUser']) {
					script {
						GET_BUILD_USER = "${BUILD_USER}"
					}
				}
				script {
					timeout(time: "${abortTimer}", unit: "SECONDS") {
						input message: "Are you sure to ${params.operationType} ${repositoryName} on ${params.remoteServer}?", ok: 'Proceed'
					}
				}
			}
		}

		stage('dockerComposeBuildUp') {
			when {
				expression {
					params.operationType == 'dockerComposeBuildUp'
				}
			}
			agent {
				label "jenkins-reserved"
			}
			steps {
				script {
					stage('gitPull') {
						gitPullRepo()
					}
					stage('copyRepoToRemote') {
						copyRepo()
					}
					stage('dockerComposeDown') {
						dockerComposeDown()
					}
					stage('dockerComposeBuild') {
						dockerComposeBuild()
					}
					stage('dockerComposeUp') {
						dockerComposeUp()
					}
				}
			}
		}

		stage('dockerComposeBuild') {
			when {
				expression {
					params.operationType == 'dockerComposeBuild'
				}
			}
			agent {
				label "jenkins-reserved"
			}
			steps {
				script {
					stage('gitPull') {
						gitPullRepo()
					}
					stage('copyRepoToRemote') {
						copyRepo()
					}
					stage('dockerComposeDown') {
						dockerComposeDown()
					}
					stage('dockerComposeBuild') {
						dockerComposeBuild()
					}
				}
			}
		}

		stage('dockerComposeDown') {
			when {
				expression {
					params.operationType == 'dockerComposeDown'
				}
			}
			agent {
				label "jenkins-reserved"
			}
			steps {
				script {
					stage('dockerComposeDown') {
						dockerComposeDown()
					}
				}
			}
		}

		stage('dockerComposeUp') {
			when {
				expression {
					params.operationType == 'dockerComposeUp'
				}
			}
			agent {
				label "jenkins-reserved"
			}
			steps {
				script {
					stage('dockerComposeUp') {
						dockerComposeUp()
					}
				}
			}
		}

	post {
		always {
			script {
				if (currentBuild.currentResult != 'ABORTED') {
					sendMail("The ${repositoryName} ${params.operationType} on ${params.remoteServer} by ${GET_BUILD_USER} build:${BUILD_NUMBER} ${currentBuild.currentResult}", "'Deploy logs:'\"<BR />\"${BUILD_URL}console\"<BR />\"${buildLogBlue}")
					postTeamsMessage("The ${repositoryName} ${params.operationType} deployEnv:${params.targetEnvironment} git:${params.gitBranch} ${params.gitTAG} app:${params.buildApp} is ${currentBuild.currentResult}")
				}
			}
		}
    }
}
