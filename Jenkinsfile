pipeline {
    agent any 
    stages{
        stage("Test-Application"){
            steps{
                sh './jenkins/test.sh'
            }
        }
        
        
        
        stage("Build-Images"){
            steps{
                sh './jenkins/build-images.sh'
            }
        }
        
        
        stage("Deploy-Services"){
            steps{
                sh './jenkins/deploy.sh'
            }
        }                   
