import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = dict()
    linked_pages = corpus[page]
    # Initialise probability distribution with probability 0.15 among all pages.
    for page in corpus.keys():
        model[page] = (1- DAMPING) / len(corpus)
    # Add additional probability for all pages linked to the current page.
    if linked_pages:
        for page in linked_pages:
            model[page] += ( DAMPING / len(linked_pages) )
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize Dictionary to store pagerank with value 0 for all corpus pages
    page_ranks = dict()
    for page in corpus:
        page_ranks[page] = 0
        
    # start by choosing a page at random
    next_page = random.choice(list(corpus))
    for i in range(n):
        # get the probabilities for the next sample
        model = transition_model(corpus, next_page, damping_factor)
        # get the next sample at random with weights of the probabilities of the next sample
        next_page = random.choices(list(model), weights=model.values(), k=1).pop()
        # keep track of how many times we’ve visited each page/sample.
        page_ranks[next_page] += 1
    # an estimate for that page’s rank (Divide the number of times surfer landed at one page by the sample size)
    for page in page_ranks:
        page_ranks[page] = page_ranks[page] / n
    
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict()
    # assigning each page a rank of 1 / N
    for page in corpus:
        page_ranks[page] = 1 / len(corpus)    
    # keep track of the differences , due to no PageRank value changes by more than 0.001
    converged = False
    while not converged:
        pageranks_copy = page_ranks.copy()
        diff_list = set()
        
        for page in corpus:
            old_rank = page_ranks[page]
            # define probability to calculate the summation
            probability = 0            
            # Summation: PR(i) / NumLinks(i)
            for page_i, pages in corpus.items():
                # Check if current page has a link to our page p
                if page in pages:
                    # Use previous pagerank for summation
                    probability += pageranks_copy[page_i] / len(pages)
                # A page that has no links at all interpreted as having one link for every page in the corpus (including itself).
                elif len(pages) == 0:
                    probability += 1 / len(corpus)
                
            # calculate new rank value
            page_ranks[page] = (1 - damping_factor) / len(corpus) + (damping_factor * probability)
            # keep track of the differences
            diff = abs(page_ranks[page] - old_rank)
            diff_list.add(diff)
            
        converged = True
        for diff in diff_list:
            if diff > 0.001:
                converged = False

    # Important normaliziation due to if the pageranks do not sum up and thus need to be normalized
    # by dividing each pagerank with their overall sum
    sum_pagerank = 0
    for p in page_ranks:
        sum_pagerank += page_ranks[p]
        
    for p in page_ranks:
        page_ranks[p] = page_ranks[p] / sum_pagerank
        
    return page_ranks
            

if __name__ == "__main__":
    main()