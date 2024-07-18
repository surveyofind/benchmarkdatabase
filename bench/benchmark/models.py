from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    gdc = models.BooleanField('gdc', default=False)
    cors = models.BooleanField('sbm', default=False)
    



class gtstation(models.Model):
    keyid = models.CharField(max_length=200,blank=True, null=True)
    gtstation_name = models.CharField(max_length=200,blank=True, null=True)
    pamphlet_no = models.CharField(max_length=200,blank=True, null=True)
    state = models.CharField(max_length=200,blank=True, null=True)
    ellipsoidheight = models.CharField(max_length=200,blank=True, null=True)
    triangulatedheight = models.CharField(max_length=200,blank=True, null=True)
    orthometrichight = models.CharField(max_length=200,blank=True, null=True)
    gravityvalue = models.CharField(max_length=200,blank=True, null=True)
    district = models.CharField(max_length=200,blank=True, null=True)
    tahsil = models.CharField(max_length=200,blank=True, null=True)
    pincode = models.CharField(max_length=200,blank=True, null=True)
    longitude = models.CharField(max_length=200,blank=True, null=True)
    latitude = models.CharField(max_length=200,blank=True, null=True)
    gt_station_inscription = models.CharField(max_length=200,blank=True, null=True)
    old_description = models.TextField(blank=True, null=True)
    revised_description = models.TextField(blank=True, null=True)
    conduction_of_gtstation = models.CharField(max_length=500,blank=True, null=True)
    image_east = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_west = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_north = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_south = models.ImageField(upload_to ='image/',blank=True, null=True)
    authorised_person_name_and_designation = models.CharField(max_length=500,blank=True, null=True)
    authorised_person_contactno = models.CharField(max_length=500,blank=True, null=True) 
    last_date_of_vist = models.CharField(max_length=500,blank=True, null=True)
    inspection_remark = models.CharField(max_length=500,blank=True, null=True)
    updatetime = models.CharField(max_length=500,blank=True, null=True)
    gdc_username = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.keyid:
            last_entry = gtstation.objects.all().order_by('id').last()
            if last_entry:
                last_keyid = last_entry.keyid
                new_keyid = int(last_keyid[3:]) + 1
                self.keyid = 'GTS' + str(new_keyid).zfill(4)
            else:
                self.keyid = 'GTS0001'
        super(gtstation, self).save(*args, **kwargs)


class gcpdata(models.Model):
    keyid = models.CharField(max_length=200,blank=True, null=True)
    gcp_name = models.CharField(max_length=200,blank=True, null=True)
    pamphlet_no = models.CharField(max_length=200,blank=True, null=True)
    state = models.CharField(max_length=200,blank=True, null=True)
    district = models.CharField(max_length=200,blank=True, null=True)
    tahsil = models.CharField(max_length=200,blank=True, null=True)
    pincode = models.CharField(max_length=200,blank=True, null=True)
    longitude = models.CharField(max_length=200,blank=True, null=True)
    latitude = models.CharField(max_length=200,blank=True, null=True)
    ellipsoidheight = models.CharField(max_length=200,blank=True, null=True)
    orthometrichight = models.CharField(max_length=200,blank=True, null=True)
    gravityvalue = models.CharField(max_length=200,blank=True, null=True)
    gcp_on_pillar =  models.CharField(max_length=500,blank=True, null=True)
    old_description = models.TextField(blank=True, null=True)
    revised_description = models.TextField(blank=True, null=True)
    conduction_of_gcp = models.CharField(max_length=500,blank=True, null=True)
    image_east = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_west = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_north = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_south = models.ImageField(upload_to ='image/',blank=True, null=True)
    authorised_person_name_and_designation = models.CharField(max_length=500,blank=True, null=True)
    authorised_person_contactno = models.CharField(max_length=500,blank=True, null=True) 
    last_date_of_vist = models.CharField(max_length=500,blank=True, null=True)
    inspection_remark = models.CharField(max_length=500,blank=True, null=True)
    updatetime = models.CharField(max_length=500,blank=True, null=True)
    gdc_username = models.TextField(blank=True, null=True)
    pid = models.CharField(max_length=500,blank=True, null=True)

class sbmdata(models.Model):
    keyid = models.CharField(max_length=200,blank=True, null=True)
    sbm_type = models.CharField(max_length=200,blank=True, null=True)
    pamphlet_no = models.CharField(max_length=200,blank=True, null=True)
    state = models.CharField(max_length=200,blank=True, null=True)
    district = models.CharField(max_length=200,blank=True, null=True)
    tahsil = models.CharField(max_length=200,blank=True, null=True)
    pincode = models.CharField(max_length=200,blank=True, null=True)
    longitude = models.CharField(max_length=200,blank=True, null=True)
    latitude = models.CharField(max_length=200,blank=True, null=True)
    sbm_inscription =  models.CharField(max_length=500,blank=True, null=True)
    old_description = models.CharField(max_length=500,blank=True, null=True)
    revised_description = models.CharField(max_length=500,blank=True, null=True)
    conduction_of_sbm = models.CharField(max_length=500,blank=True, null=True)
    conduction_of_reference_pillar = models.CharField(max_length=500,blank=True, null=True)
    image_east = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_west = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_north = models.ImageField(upload_to ='image/',blank=True, null=True)
    image_south = models.ImageField(upload_to ='image/',blank=True, null=True)
    authorised_person_name_and_designation = models.CharField(max_length=500,blank=True, null=True)
    authorised_person_contactno = models.CharField(max_length=500,blank=True, null=True) 
    last_date_of_vist = models.CharField(max_length=500,blank=True, null=True)
    inspection_remark = models.CharField(max_length=500,blank=True, null=True)
    updatetime = models.CharField(max_length=500,blank=True, null=True)
    gdc_username = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.keyid:
            last_entry = sbmdata.objects.all().order_by('id').last()
            if last_entry:
                last_keyid = last_entry.keyid
                new_keyid = int(last_keyid[3:]) + 1
                self.keyid = 'SBM' + str(new_keyid).zfill(4)
            else:
                self.keyid = 'SBM0001'
        super(sbmdata, self).save(*args, **kwargs)
 



    

class BenchmarkSbmdataBackup(models.Model):
    keyid = models.CharField(max_length=200, blank=True, null=True)
    sbm_type = models.CharField(max_length=200, blank=True, null=True)
    pamphlet_no = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    tahsil = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    sbm_inscription = models.CharField(max_length=500, blank=True, null=True)
    old_description = models.CharField(max_length=500, blank=True, null=True)
    revised_description = models.CharField(max_length=500, blank=True, null=True)
    conduction_of_sbm = models.CharField(max_length=500, blank=True, null=True)
    conduction_of_reference_pillar = models.CharField(max_length=500, blank=True, null=True)
    image_east = models.CharField(max_length=500, blank=True, null=True)
    image_west = models.CharField(max_length=500, blank=True, null=True)
    image_north = models.CharField(max_length=500, blank=True, null=True)
    image_south = models.CharField(max_length=500, blank=True, null=True)
    authorised_person_name_and_designation = models.CharField(max_length=500, blank=True, null=True)
    authorised_person_contactno = models.CharField(max_length=500, blank=True, null=True)
    last_date_of_vist = models.CharField(max_length=500, blank=True, null=True)
    inspection_remark = models.CharField(max_length=500, blank=True, null=True)
    updatetime = models.CharField(max_length=500, blank=True, null=True)
    gdc_username = models.TextField(blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'benchmark_sbmdata_backup'


class BenchmarkGcpdataBackup(models.Model):
    keyid = models.CharField(max_length=200, blank=True, null=True)
    gcp_name = models.CharField(max_length=200, blank=True, null=True)
    pamphlet_no = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    tahsil = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    ellipsoidheight = models.CharField(max_length=200, blank=True, null=True)
    orthometrichight = models.CharField(max_length=200, blank=True, null=True)
    gravityvalue = models.CharField(max_length=200, blank=True, null=True)
    gcp_on_pillar = models.CharField(max_length=500, blank=True, null=True)
    old_description = models.TextField(blank=True, null=True)
    revised_description = models.TextField(blank=True, null=True)
    conduction_of_gcp = models.CharField(max_length=500, blank=True, null=True)
    image_east = models.CharField(max_length=500, blank=True, null=True)
    image_west = models.CharField(max_length=500, blank=True, null=True)
    image_north = models.CharField(max_length=500, blank=True, null=True)
    image_south = models.CharField(max_length=500, blank=True, null=True)
    authorised_person_name_and_designation = models.CharField(max_length=500, blank=True, null=True)
    authorised_person_contactno = models.CharField(max_length=500, blank=True, null=True)
    last_date_of_vist = models.CharField(max_length=500, blank=True, null=True)
    inspection_remark = models.CharField(max_length=500, blank=True, null=True)
    updatetime = models.CharField(max_length=500, blank=True, null=True)
    gdc_username = models.TextField(blank=True, null=True)
    pid = models.CharField(max_length=500, blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'benchmark_gcpdata_backup'


class BenchmarkGtstationBackup(models.Model):
    keyid = models.CharField(max_length=200, blank=True, null=True)
    gtstation_name = models.CharField(max_length=200, blank=True, null=True)
    pamphlet_no = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    ellipsoidheight = models.CharField(max_length=200, blank=True, null=True)
    triangulatedheight = models.CharField(max_length=200, blank=True, null=True)
    orthometrichight = models.CharField(max_length=200, blank=True, null=True)
    gravityvalue = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    tahsil = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    gt_station_inscription = models.CharField(max_length=200, blank=True, null=True)
    old_description = models.TextField(blank=True, null=True)
    revised_description = models.TextField(blank=True, null=True)
    conduction_of_gtstation = models.CharField(max_length=500, blank=True, null=True)
    image_east = models.CharField(max_length=500, blank=True, null=True)
    image_west = models.CharField(max_length=500, blank=True, null=True)
    image_north = models.CharField(max_length=500, blank=True, null=True)
    image_south = models.CharField(max_length=500, blank=True, null=True)
    authorised_person_name_and_designation = models.CharField(max_length=500, blank=True, null=True)
    authorised_person_contactno = models.CharField(max_length=500, blank=True, null=True)
    last_date_of_vist = models.CharField(max_length=500, blank=True, null=True)
    inspection_remark = models.CharField(max_length=500, blank=True, null=True)
    updatetime = models.CharField(max_length=500, blank=True, null=True)
    gdc_username = models.TextField(blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'benchmark_gtstation_backup'













           