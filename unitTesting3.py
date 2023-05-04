import os
import sys
import unittest
import HtmlTestRunner
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.language.questionanswering import QuestionAnsweringClient

load_dotenv()
endpoint = os.environ.get('AA_QA_ENDPOINT')
credential = AzureKeyCredential(os.environ.get('AA_QA_KEY'))
knowledge_base_project = os.environ.get('AA_QA_KB')
deployment = "test"


class TestQuestionAnswering(unittest.TestCase):

    def setUp(self):
        self.question = 'java exceptions?'

    def test_language_detection(self):
        ld_client = TextAnalyticsClient(endpoint, credential)
        lang = ld_client.detect_language(documents=[self.question])[0].primary_language.name
        self.assertEqual(lang, 'English')

    def test_get_answers(self):
        qa_client = QuestionAnsweringClient(endpoint, credential)
        with qa_client:
            response = qa_client.get_answers(
                question=self.question,
                confidence_threshold=0.5,
                top=3,
                project_name=knowledge_base_project,
                deployment_name=deployment
            )
        self.assertNotEqual(response.answers[0].qna_id, -1)

    def test_chitchat_answer(self):
        qa_client = QuestionAnsweringClient(endpoint, credential)
        with qa_client:
            response = qa_client.get_answers(
                question='Hi',
                confidence_threshold=0.5,
                top=3,
                project_name=knowledge_base_project,
                deployment_name=deployment
            )
        self.assertTrue(any('chitchat' in answer.source for answer in response.answers))


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test-reports'))
