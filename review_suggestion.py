import pygit2
import argparse
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE


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
        current_diff = commit.tree.diff_to_tree(commit.parents[0].tree)
        for patch in current_diff:
            filename = patch.delta.old_file.path
            changed_files.add(filename) 

    print('Changed files: ')
    print(changed_files)

    # Now changed_files set contains names of all the changed files, iterate through all other commits 
    # and compare them to the review commits, calculate similarity scores for authors
    for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
        if not commit.parents:
            print('No commit parents for commit: ', commit.id.__str__(), ', assuming no changed files')
            continue
        past_commits_changed_files = set()
        if (commit.id.__str__() not in review_commit_hashes):
            current_diff = commit.tree.diff_to_tree(commit.parents[0].tree)
            for patch in current_diff:
                
                filename = patch.delta.old_file.path
                past_commits_changed_files.add(filename)
            commit_similarity_score = jaccard_index(changed_files, past_commits_changed_files)
            if commit.author.email != review_author:  
                if commit.author.email in authors:
                    authors[commit.author.email] += commit_similarity_score
                else:
                    authors[commit.author.email] = commit_similarity_score
                print('Commit No: ', commit.id.__str__(), '; Similarity score of ', commit_similarity_score, ' added to author: ', commit.author.email)


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