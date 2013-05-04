from django.db import models
	

class Region(models.Model):
	REGION_CHOICES = (
		("n", "North America"),
		("e", "Europe"),
		("a", "Asia"),
	)
	region = models.CharField(max_length=1, choices=REGION_CHOICES, db_index=True)
	
	def __unicode__(self):
		return self.region
	
class Tier(models.Model):
	TIER_CHOICES = (
		("l", "Laptop"),
		("d", "Desktop"),
		("m", "Mobile"),
	)
	tier = models.CharField(max_length=1, choices=TIER_CHOICES, db_index=True)
	cost = models.IntegerField(db_index=True)
	
	def __unicode__(self):
		return self.tier
	
class Device(models.Model):
	tier = models.ForeignKey(Tier, db_index=True)
	region = models.ForeignKey(Region, db_index=True)
	count = models.IntegerField(db_index=True)

	def __unicode__(self):
		return self.id
	
class Demand(models.Model):
	region = models.ForeignKey(Region, db_index=True)
	count = models.IntegerField(db_index=True)
	
	def __unicode__(self):
		return self.region + ' ' + str(self.count)
	

class Profit(models.Model):
	last_profit = models.IntegerField(db_index=True)
	last_potential = models.IntegerField(db_index=True)
	total_profit = models.IntegerField(db_index=True)
	potential = models.IntegerField(db_index=True)
	
class Turn(models.Model):
	config = models.ManyToManyField(Device, related_name='config', verbose_name='current distribution')
	demands = models.ManyToManyField(Demand, verbose_name="list of demands")
	distribution = models.ManyToManyField(Device, related_name='distribution', verbose_name="distribution of the last turn")
	profit = models.ForeignKey(Profit, db_index=True)
	control = models.ManyToManyField(Device, related_name='control',verbose_name="our move")
	revenue_cents = models.IntegerField(db_index=True)

	

	


	

	

