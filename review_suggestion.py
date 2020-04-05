import pygit2
import argparse


def reccomend_reviewer(path, review_commit_hashes):
    '''Takes a path to a local git repository, and a list of commit ids in hexidecimal 
       and returns a list of 5 most relevant reccomended reviewers for those commits'''
    changed_files = set()
    authors = {}
    repo = pygit2.Repository(path)
    review_author = repo.get(review_commit_hashes[0]).author.email

    # Firstly let's identify the files that have been changed in the review commits
    for hash in review_commit_hashes:
        commit = repo.get(hash)
        for obj in commit.tree:
            if obj.type == pygit2.GIT_OBJ_BLOB:
                changed_files.add(obj.name)

    # Now changed_files set contains names of all the changed files, iterate through all other commits 
    # and compare them to the review commits, calculate similarity scores for authors
    for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL | pygit2.GIT_SORT_REVERSE):
        past_commits_changed_files = set()
        if (commit.id.__str__() not in review_commit_hashes):
            for obj in commit.tree:
                if obj.type == pygit2.GIT_OBJ_BLOB:
                    if obj.name in changed_files:
                        past_commits_changed_files.add(obj.name)
            commit_similarity_score = jaccard_index(changed_files, past_commits_changed_files)
            if commit.author.email != review_author:  
                if commit.author.email in authors:
                    authors[commit.author.email] += commit_similarity_score
                else:
                    authors[commit.author.email] = commit_similarity_score

    # Lastly sort authors by their accumulated relevance score, and output top 5
    suggested_reviewers = {k: v for k, v in sorted(authors.items(), key=lambda item: item[1], reverse=True)}
    return list(suggested_reviewers.keys())[:5]
        

def jaccard_index(set1, set2):
    '''Takes two sets and returns Jaccard Similarity Index for them'''
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return float(intersection) / float(union)

def main():
    parser = argparse.ArgumentParser(description='Input a local github repo path and a list of commit hashes comprising a code review')
    parser.add_argument('repo_path', type=str, help='Path to local github repository, must not be a path to the repositorys working dir and therefore must end with /.git')
    parser.add_argument('hashes_list', nargs='+', type=str, help='A list of hexidecimal hashes of commits to be included in a review')
    args = parser.parse_args()
    list_of_reviewers = reccomend_reviewer(args.repo_path, args.hashes_list)
    print("\n")
    print("Top 5 recommended reviewers:\n")
    print(list_of_reviewers)
    print("\n")

if __name__ == '__main__':
    main()