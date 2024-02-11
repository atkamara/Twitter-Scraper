import numpy,tqdm

from utils                                    import SearchAuto,readJSONfiles,compute_intervals


class process:

    def __init__(self,
                 n_branches,
                 TWXT_output,
                 output):
        self.n_branches                          = int(n_branches)
        self.TWXT_output                         = TWXT_output
        self.JSONfiles                           = readJSONfiles(self.TWXT_output)
        self.output                              = output
    def split_into_branches(self):
        intervals                                = compute_intervals(**self.JSONfiles['Search'])
        self.intervals                           = [v.tolist() 
                                                   for _id,v in enumerate(numpy.array_split(intervals, self.n_branches))] 
    def scroll_intervals_for_branch_id(self,
                                   branch_id)    :
        branch_intervals                         = self.intervals[branch_id]
        for interval in tqdm.tqdm(
                           branch_intervals)     :
            JSONfiles_for_interval               = self.JSONfiles
            JSONfiles_for_interval[
            'Search'].update(  {"start_date"     : interval[0],
                                  "end_date"     : interval[1]})
            SearchAuto(
                output = self.output,
                **JSONfiles_for_interval
                     ).scroll()

if __name__ == "__main__":
    import sys
    from multiprocessing import Pool
    options                                  = dict( 
                                               map(lambda opt: opt.split('='),
                                               sys.argv[1:]))
    scroll_process                           = process(**options)
    scroll_process.split_into_branches()
    n_branches                               = int(options['n_branches'])
    with Pool(n_branches)     as p:
        p.map(
            scroll_process.scroll_intervals_for_branch_id, 
            list(range(n_branches)))