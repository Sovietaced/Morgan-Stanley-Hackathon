
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
		("w", "Web"),
		("j", "Java"),
		("d", "Database"),
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
		return 'Device : ' + str(self.id) + " Region : " + self.region.region + " Count : " + str(self.count) + " Tier : " + self.tier.tier

class Demand(models.Model):
	region = models.ForeignKey(Region, db_index=True)
	count = models.IntegerField(db_index=True)

	def __unicode__(self):
		return self.region.region + ' ' + str(self.count)


class Profit(models.Model):
	last_profit = models.IntegerField(db_index=True)
	last_potential = models.IntegerField(db_index=True)
	total_profit = models.IntegerField(db_index=True)
	total_potential = models.IntegerField(db_index=True)

	def __unicode__(self):
		return "Profit ID : " + str(self.id) + " last_profit : " + str(self.last_profit) + " last_potential : " + str(self.last_potential) + " total_profit : " + str(self.total_profit) + " total_potential : " + str(self.total_potential)

class Turn(models.Model):
	time = models.DateTimeField(null=True, blank=True, db_index=True)
	config = models.ManyToManyField(Device, blank=True, related_name='cfg', verbose_name='current distribution')
	demands = models.ManyToManyField(Demand, null=True, blank=True, verbose_name="list of demands")
	distribution = models.ManyToManyField(Device, null=True, blank=True, related_name='distribution', verbose_name="distribution of the last turn")
	profit = models.ForeignKey(Profit, null=True, blank=True, db_index=True)
	control = models.ManyToManyField(Device, null=True,blank=True, related_name='control',verbose_name="our move")
	revenue_cents = models.IntegerField(blank=True, null=True, db_index=True)

	def __unicode__(self):
		return 'Time: ' + str(self.time)



if __name__ == "__main__" and __package__ is None:
    __package__ = "hackathon.models"
