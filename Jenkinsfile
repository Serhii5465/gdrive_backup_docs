@Library('PrepEnvForBuild') _

pipeline{
    agent {
        label 'master'
    }
    
    options { 
        skipDefaultCheckout() 
    }

    parameters {
        choice choices: ['Win10_MSI', 'Win10-Dell'], description: 'Choose an agent for deployment', name: 'AGENT'
    }

    stages {
        stage('Check status agent'){
            steps{
                CheckAgent("${params.AGENT}")
            }
        }

        stage('Git checkout'){
            steps {
                checkout scmGit(branches: [[name: 'main']],
                extensions: [], 
                userRemoteConfigs: [[url: 'gdrive_backup_docs_repo:Serhii5465/gdrive_backup_docs.git']])

                stash includes: '*.py', name: 'src'
            }
        }

        stage ('Deploy'){
            agent {
                label "${params.AGENT}"
            }
            steps {
                unstash 'src'
                bat returnStatus: true, script: 'Robocopy.exe /copyall . D:\\system\\applications\\cygwin64\\home\\raisnet\\scripts\\gdrive_backup_docs'
            }
        }
    }
}