@Library(['PrepEnvForBuild', 'DeployWinAgents']) _

node('master') {
    def config = [
        platform: "win32",
        git_repo_url : "git@github.com:Serhii5465/gdrive_backup_docs.git",
        git_branch : "main",
        git_cred_id : "gdrive_backup_docs_repo_cred",
        stash_includes : "**/*.py",
        stash_excludes : "",
        command_deploy : "robocopy /E . D:\\system\\scripts\\gdrive_backup_docs",
        func_deploy : ""
    ]

    DeployArtifactsPipelineOnAgents(config)
}