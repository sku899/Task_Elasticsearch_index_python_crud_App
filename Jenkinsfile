pipeline {
    agent any 
    stages{
        stage("Test"){
            steps{
                sh './scripts/test.sh'
            }
        }
        
        
        
        stage("Build-Images"){
            steps{
                sh './scripts/build-images.sh'
            }
        }
        
        
        stage("Deploy"){
            steps{
                sh './scripts/deploy.sh'
            }
        }                   
