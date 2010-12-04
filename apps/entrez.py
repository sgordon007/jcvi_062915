"""
Wrapper for calling Bio.Entrez tools to get the sequence from a list of IDs
"""

import sys
import logging

from optparse import OptionParser
from Bio import Entrez

email = "htang@jcvi.org"


def batch_entrez(list_of_terms, db="nucleotide", retmax=1, rettype="fasta"):
    """
    Retrieving multiple rather than a single record
    """

    for term in list_of_terms:

        logging.debug("search term %s" % term)
        search_handle = Entrez.esearch(db=db, retmax=retmax, term=term,
                email=email)
        rec = Entrez.read(search_handle)
        ids = rec["IdList"]

        if not ids:
            logging.error("term %s not found in db %s" % (term, db))

        for id in ids:
            fetch_handle = Entrez.efetch(db=db, id=id, rettype=rettype,
                    email=email)
            yield fetch_handle.read()


def main():
    """
    %prog filename

    filename contains a list of terms to search 
    """
    logging.basicConfig(level=logging.DEBUG)

    p = OptionParser(main.__doc__)
    opts, args = p.parse_args()

    if len(args) != 1:
        sys.exit(p.print_help())

    filename = args[0]
    list_of_terms = [row.strip() for row in open(filename)]
    for rec in batch_entrez(list_of_terms):
        print rec


if __name__ == '__main__':
    main()
