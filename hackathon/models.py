from django.db import models

# Create your models here.
class Device(models.Model):
	tier = models.ForeignKey(Tier, db_index=True)
	region = models.ForeignKey(Region, db_index=True)	
	count = models.IntegerField(db_index=True)
	createdAt = models.DateTimeField(auto_now=True)
	updatedAt = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.id
	

class Tier(models.Model):
	TIER_CHOICES = (
		("l", "Laptop"),
		("d", "Desktop"),
		("m", "Mobile"),
	)
	tier = models.CharField(max_length=1, choices=TIER_CHOICES, db_index=True)
	cost = models.IntegerField(db_index=True)
	
class Region(models.Model):
	REGION_CHOICES = (
		("n", "North America"),
		("e", "Europe"),
		("a", "Asia"),
	)
	region = models.CharField(max_length=1, choices=REGION_CHOICES, db_index=True)
	
class Decision(models.Model):
	devices = models.ManyToManyField(Device, verbose_name="list of devices")
	demands = models.ManyToManyField(Demand, verbose_name="list of demands")
	
	
class Demand(models.Model):
	region = models.ForeignKey(Region, db_index=True)
	count = models.IntegerField(db_index=True)
	
class Distribution(models.Model):
	devices = models.ManyToManyField(Device, verbose_name="list of devices")

class Profit(models.Model):
	

	

	


	

	

