getPullRequestsQuery = """
            {
                search(
                    query: \"type:pr repo:nameWithOwner state:closed state:merged\"
                    type: ISSUE
                    first: 30
                    after: null
                ) {
                    pageInfo {
                        endCursor
                        startCursor
                    }
                    nodes {
                        ... on PullRequest {
                            repository {
                                owner {
                                    login
                                }
                                name
                            }
                            title
                            state
                            createdAt
                            mergedAt
                            closedAt
                            bodyText
                            reviews { totalCount }
                            comments { totalCount } 
                            participants { totalCount }
                            changedFiles
                            additions
                            deletions
                            number
                            id
                        }
                    }
                }
            }
        """
        
getRepositoriesQuery = """
    {
        search(
            query: "stars:>100"
            type: REPOSITORY
            first: 20
            after: null
        ) {
            pageInfo {
            endCursor
            startCursor
            }
            nodes {
                ... on Repository {
                    nameWithOwner
                    closedPRs: pullRequests(states: CLOSED, first: 1) {
                        totalCount
                    }
                    mergedPRs: pullRequests(states: MERGED, first: 1) {
                        totalCount
                    }
                }
            }
        }
    }
    """