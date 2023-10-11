import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler

class RulerModel():
    def __init__(self, surgery, internalMedicine, medication, obstetricsGynecology):
        self.ruler_model = spacy.blank('en')
        self.entity_ruler = self.ruler_model.add_pipe('entity_ruler')

        all_patterns = []

        pattern = self.create_patterns(surgery, 'surgery')
        all_patterns.extend(pattern)
        pattern = self.create_patterns(internalMedicine, 'internalMedicine')
        all_patterns.extend(pattern)
        pattern = self.create_patterns(medication, 'medication')
        all_patterns.extend(pattern)
        pattern = self.create_patterns(obstetricsGynecology, 'obstetricsGynecology')
        all_patterns.extend(pattern)

        self.add_patterns_into_ruler(all_patterns)
        self.save_ruler_model()

    def create_patterns(self, entity_type_set, entity_type):
            patterns = []
            for item in entity_type_set:
                pattern = {'label': entity_type, 'pattern': item}
                patterns.append(pattern)
            
            return patterns
        
    def add_patterns_into_ruler(self, total_patterns):
            self.entity_ruler.add_patterns(total_patterns)