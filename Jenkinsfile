@Library(['PrepEnvForBuild', 'DeployWinAgents']) _

node('master') {
    def raw = libraryResource 'configs/gdrive_backup_docs_repo.json'
    def config = readJSON text: raw
    DeployArtifactsPipelineWinAgents(config)
}