from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Indication(models.Model):
    """Model representing a medication indication"""
    name = models.CharField(max_length=200, help_text='Enter a medication indication (ex: hypertension)')
    plainlang = models.CharField(max_length=200, help_text='Enter a patient-friendly descriptor for the indication (e.g. "blood pressure" for hypertension)')

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
        
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Frequency(models.Model):
	abbr_frequency = models.CharField(max_length = 5, help_text='Write out the frequency in abbreviated form (e.g. QD, BID, TID, etc.)')
	long_frequency = models.CharField(max_length = 200, help_text='Write out the frequency in a patient-friendly format all lowercase without abbreviations')
	
	class Meta:
		ordering = ['abbr_frequency']
		
	def __str__(self):
		return self.abbr_frequency
	
class Route(models.Model):
	abbr_route = models.CharField(max_length = 5, help_text='Write the route in abbreviated form (ex: PO, SQ, etc.)')
	long_route = models.CharField(max_length = 100, help_text='Write the route in a patient-friendly form')
	
	class Meta:
		ordering = ['abbr_route']
		
	def __str__(self):
		return self.abbr_route
    
class MedQualifiers(models.Model):
    name = models.CharField(max_length=50, verbose_name="Medication Qualifiers", help_text="Enter a commonly recognized abbreviation for this qualifier (e.g. XR for Extended Release)")
    terms = models.TextField(max_length=500, verbose_name="Similar Qualifier Terms", help_text="Enter any other terms that relate to this qualifier, separated by commas (for XR, also enter DR, SR, CR, etc)")

	class Meta:
		ordering = ['med_qualifier']
		
	def __str__(self):
		return self.med_qualifier

class Med(models.Model):
    """Model representing a medication but not a specific patient's medication'"""
    
    generic_name = models.CharField(max_length=200)
    match_1st = models.CharField(max_length=200, blank=True null=True)
    match_2nd = models.CharField(max_length=200, blank=True null=True)
    qualifiers = models.ManyToManyField('MedQualifiers', blank=True, null=True, help_text="Add any terms that will help distinguish this medication from other similar medications such as forumalation or strength")
    phonetic_name = models.CharField(max_length=200, help_text='Spell the medication name phonetically')
    trade_name = models.CharField(max_length=200, help_text='Brand name of the medication')
    med_class = models.ForeignKey('Med_Class', verbose_name='Medication Class', help_text='Enter the name of the medication class', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    dose = models.CharField('Dose', max_length = 10)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True) 
    mechanism_of_action = models.TextField(max_length=1000, help_text='Enter a brief description of the mechanism of action')
    notes = models.TextField(max_length=500, help_text='Enter any additional notes')
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    indication = models.ManyToManyField(Indication, help_text='Select an indication for this medication')
    
    class Meta:
        ordering = ['medication_name']
        
    def display_indication(self):
        """Create a string for the indication. This is required to display indication in Admin."""
        return ', '.join(indication.name for indication in self.indication.all()[:3])
    
    display_indication.short_description = 'Indication'
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.medication_name}, {self.dose}, {self.route}'
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this med"""
        return reverse('med-detail', args=[str(self.id)])

import uuid # Required for unique book instances

class MedInstance(models.Model):
    """Model representing a specific patients script for this med."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular prescription across whole database')
    med = models.ForeignKey('Med', on_delete=models.SET_NULL, null=True) 
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True)
    frequency = models.ForeignKey(Frequency, on_delete=models.SET_NULL, null=True)
    date_prescribed = models.DateField(null=True, blank=True)
    date_filled = models.DateField(null=True, blank=True)
    prescriber = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    MED_STATUS = (
        ('a', 'Adherent'),
        ('u', 'Unsure'),
        ('n', 'Not Adherent'),
        ('o', 'Out of Medication'),
    )

    status = models.CharField(
        max_length=1,
        choices=MED_STATUS,
        blank=True,
        default='m',
        help_text='Medication Status',
    )

    class Meta:
        ordering = ['date_filled']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.patient}, {self.med.medication_name})'
        
class Patient(models.Model):
    """Model representing a patient"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('patient-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

class Med_Class(models.Model):
    class_name = models.CharField(max_length=100, verbose_name='Medication Class', help_text='Enter a medication class')
    interactions = models.ManyToManyField('Med_Class', verbose_name='Interactions', help_text='Enter the classes this medication interacts with',blank=True, null=True)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this med"""
        return reverse('med-class', args=[str(self.id)])