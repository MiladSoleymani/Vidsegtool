class Job:
    def __init__(self, name, stage, func, next_job_names=None):
        self.name = name
        self.stage = stage
        self.func = func
        self.next_job_names = next_job_names
    
    def __call__(self):
        self.func()

class Pipeline:
    def __init__(self, jobs: list[Job]):
        _jobs_names = [j.name for j in jobs]
        assert len(_jobs_names) == len(set(_jobs_names))
        self.name_job_mapping = {job.name: job for job in jobs}
    
    def get_next_job(self, job_names: set):
        next_job = list(
            sorted(
                [self.name_job_mapping[jn] for jn in job_names], key=lambda job: job.stage
            )
        )
        if not next_job:
            return None
        next_job = next_job[0]

        job_names.remove(next_job.name)
        if next_job.next_job_names:
            for name in next_job.next_job_names:
                job_names.add(name)
        return next_job

    def run(self, job_names):
        job_names = set(job_names)
        
        while job := self.get_next_job(job_names):
            job.func()
