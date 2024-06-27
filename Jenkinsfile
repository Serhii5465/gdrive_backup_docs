@Library(['PrepEnvForBuild', 'DeployWinAgents']) _

node('master') {
    def config = [
        git_repo_url : "gdrive_backup_docs_repo:Serhii5465/gdrive_backup_docs.git",
        git_branch : "main",
        stash_includes : "**/*.py",
        stash_excludes : "",
        command_deploy : "robocopy /E . D:\\system\\scripts\\gdrive_backup_docs",
        func_deploy : ""
    ]

    DeployArtifactsPipelineWinAgents(config)
}