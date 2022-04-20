import math
from multiprocessing.pool import ThreadPool

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification, \
    AutoModelForTokenClassification, pipeline

from view import View

# Model names
summarization_model = "sshleifer/distilbart-cnn-12-6"
classification_model = "distilbert-base-uncased-finetuned-sst-2-english"
ner_model = "dslim/bert-base-NER"


def download_summarization_model():
    AutoTokenizer.from_pretrained(summarization_model)
    AutoModelForSeq2SeqLM.from_pretrained(summarization_model)


def download_classification_model():
    AutoTokenizer.from_pretrained(classification_model)
    AutoModelForSequenceClassification.from_pretrained(classification_model)


def download_ner_model():
    AutoTokenizer.from_pretrained(ner_model)
    AutoModelForSequenceClassification.from_pretrained(ner_model)


def summarize(text: str, min_length: int, max_length: int) -> str:
    pipe = pipeline(task="summarization", model=summarization_model)
    summary = pipe(text, min_length=min_length, max_length=max_length)[0].get('summary_text').strip()
    return ".".join(summary.split(" .")).strip()


def classify(text: str):
    pipe = pipeline(task="text-classification", model=classification_model)
    results = pipe(text)[0]

    sentiment = results.get('label')
    confidence_level = "{0}%".format(round(results.get('score') * 100, 1))

    return sentiment, confidence_level


def named_entity_recognition(text: str):
    model = AutoModelForTokenClassification.from_pretrained(ner_model)
    tokenizer = AutoTokenizer.from_pretrained(ner_model)
    pipe = pipeline('ner', model=model, tokenizer=tokenizer)
    results = pipe(text)

    person_list = []
    organisation_list = []
    location_list = []
    misc_list = []

    def append_entity_list(_entity_name, _entity_type):
        if "PER" in _entity_type:
            person_list.append(_entity_name)

        elif "ORG" in _entity_type:
            organisation_list.append(_entity_name)

        elif "LOC" in _entity_type:
            location_list.append(_entity_name)

        elif "MIS" in _entity_type:
            misc_list.append(_entity_name)

    """
    Sample results:
    [{'entity': 'B-LOC', 'score': 0.9996414, 'index': 113, 'word': 'Northern', 'start': 598, 'end': 606}, 
    {'entity': 'I-LOC', 'score': 0.9991061, 'index': 114, 'word': 'Ireland', 'start': 607, 'end': 614}, 
    {'entity': 'B-LOC', 'score': 0.99974483, 'index': 116, 'word': 'Wales', 'start': 619, 'end': 624}, 
    {'entity': 'B-LOC', 'score': 0.9777434, 'index': 118, 'word': 'Down', 'start': 626, 'end': 630}, 
    {'entity': 'I-LOC', 'score': 0.9698499, 'index': 119, 'word': '##ing', 'start': 630, 'end': 633}, 
    {'entity': 'I-LOC', 'score': 0.9832339, 'index': 120, 'word': 'Street', 'start': 634, 'end': 640}, 
    {'entity': 'B-MISC', 'score': 0.9880397, 'index': 177, 'word': 'Co', 'start': 953, 'end': 955}, 
    {'entity': 'I-MISC', 'score': 0.7533177, 'index': 178, 'word': '##vid', 'start': 955, 'end': 958}]
    
    As we loop through the results, we will check whether each entity is connected to the entity before. If it is, we
    will combine them together.
    
    If it is not connected, we will append the previous entity name into their respective list and save the current
    entity name.
    """
    entity_name = ""
    for index, current_result in enumerate(results):

        if index == 0:
            entity_name = current_result.get("word")
            continue

        previous_result = results[index - 1]

        if current_result.get("start") - 1 == previous_result.get("end"):
            entity_name = "{0} {1}".format(entity_name, current_result.get("word"))

        elif current_result.get("start") == previous_result.get("end"):
            entity_name = "{0}{1}".format(entity_name, current_result.get("word").replace("#", ""))

        else:
            entity_type = results[index - 1].get("entity")
            append_entity_list(entity_name, entity_type)
            entity_name = current_result.get("word")

        # Save the last entity.
        if index + 1 == len(results):
            entity_type = results[-1].get("entity")
            append_entity_list(entity_name, entity_type)

    return list(set(person_list)), list(set(organisation_list)), list(set(location_list)), list(set(misc_list))


view = View()


def summarize_callback(summary):
    view.set_summary(summary)
    view.set_article_word_count(str(len(view.get_article().split())) + " words")
    view.set_summary_word_count(str(len(summary.split())) + " words")

    view.model_completed_analysis()


def classify_callback(results):
    view.set_sentiment(results[0])
    view.set_confidence(results[1])

    view.model_completed_analysis()


def ner_callback(results):
    view.set_person(", ".join(results[0]))
    view.set_organisation(", ".join(results[1]))
    view.set_location(", ".join(results[2]))
    view.set_misc(", ".join(results[3]))

    view.model_completed_analysis()


def analyse():
    view.disable_analyse_button()
    article = view.get_article()

    if view.get_option() == "PERCENTAGE":
        word_count = len(article.split())

        min_length = word_count / 100.0 * view.get_min_parameter()
        min_length = int(math.ceil(min_length))

        max_length = word_count / 100.0 * view.get_max_parameter()
        max_length = int(max_length)

    else:
        min_length = view.get_min_parameter()
        max_length = view.get_max_parameter()

    pool = ThreadPool(processes=3)
    pool.apply_async(summarize, (article, min_length, max_length), callback=summarize_callback)
    pool.apply_async(classify, (article,), callback=classify_callback)
    pool.apply_async(named_entity_recognition, (article,), callback=ner_callback)


if __name__ == '__main__':
    download_summarization_model()
    download_classification_model()
    download_ner_model()

    view.analyse_button.configure(command=analyse)
    view.run()
