from equipment.models import EquipmentInfo
from part.models import Part
from startupshot.models import startUpShot
from molds.models import Mold

class CoverPageBuilder(object):
    def __init__(self, job_number, startup_shot = None):
        self.job_number = job_number
        self.item_number_id = None
        self.machine = None
        self.mold = None
        self.part = None
        self.startup_shot = startup_shot or None
        self.job_meta = []
        self.build(job_number)

    def build(self, job_number):
        if not self.startup_shot:
            self.get_startup_shot(job_number)

        self.get_machine_info(self.startup_shot.machNo_id)
        self.get_part_info(self.startup_shot.item_id)
        self.get_mold_info(self.startup_shot.moldNumber_id)
        self.get_job_meta()
        self.get_startup_shot_meta()

    def get_job_meta(self):
        self.job_meta = []
        self.job_meta.extend([
            ['Part Number', self.part.item_Number],
            ['Part Description', self.part.item_Description],
            ['TMM Part Weight (g)', self.part.exp_part_weight],
            ['TMM Cycle (s)', self.part.exp_cycle_time],
            ['Mold Number', self.mold.mold_number],
            ['Mold Description', self.mold.mold_description],
            ['Total Cavities', self.mold.num_cavities]
        ])

    def get_machine_info(self, machine_id):
        self.machine = EquipmentInfo.objects.get(id=machine_id)

    def get_part_info(self, item_number_id):
        self.part = Part.objects.get(id=item_number_id)

    def get_startup_shot(self, job_number):
        self.startup_shot = self.startup_shot or startUpShot.objects.get(jobNumber=job_number)

    def get_startup_shot_meta(self):
        self.startup_shot_meta = []
        self.startup_shot_meta.extend([
            ['Machine Operator', self.startup_shot.machineOperator],
            ['Inspector', self.startup_shot.inspectorName],
            ['Job Number', self.startup_shot.jobNumber],
            ['Shot Weight', self.startup_shot.shotWeight],
            ['Active Cavitation', self.startup_shot.activeCavities],
            ['Average Part Weight (g)', self.startup_shot.shotWeight/self.startup_shot.activeCavities],
            ['Machine Alias', self.startup_shot.machNo],
            ['Cycle Time (s)', self.startup_shot.cycleTime],
        ])

    def get_mold_info(self, mold_id):
        self.mold = Mold.objects.get(id=mold_id)
