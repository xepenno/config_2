import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import yaml

# Импортируем функции из main.py
from main import parse_config, extract_commit_dependencies, create_mermaid_graph, save_graph_to_file

class TestDependencyVisualizer(unittest.TestCase):

    @patch('builtins.open', create=True)
    def test_parse_config(self, mock_open):
        # Подготовим mock для содержимого файла config.yaml
        mock_file = MagicMock()
        mock_file.read.return_value = """
        repo_path: "C:/Projects/config_2"
        target_file: "file_2.txt"
        output_path: "C:/Projects/config_2/output_graph.mmd"
        """
        mock_open.return_value = mock_file

        # Вызовем функцию для парсинга
        config = parse_config('C:/Projects/config_2/config.yaml')

        # Проверим, что парсинг прошел корректно
        self.assertEqual(config['repo_path'], "C:/Projects/config_2")
        self.assertEqual(config['target_file'], "file_2.txt")
        self.assertEqual(config['output_path'], "C:/Projects/config_2/output_graph.mmd")

    @patch('git.Repo')
    def test_extract_commit_dependencies(self, MockRepo):
        # Создадим mock для объекта репозитория
        mock_repo = MockRepo.return_value
        mock_commit = MagicMock()
        mock_commit.hexsha = '123abc'
        mock_commit.stats.files = {'file_2.txt': {'lines': 10}}

        # Возвращаем список из одного коммита
        mock_repo.iter_commits.return_value = [mock_commit]

        # Вызовем функцию для извлечения зависимостей
        dependency_graph = extract_commit_dependencies("C:/Projects/config_2", "file_2.txt")

        # Проверим, что зависимость была извлечена корректно
        self.assertIn('123abc', dependency_graph)
        self.assertIn('file_2.txt', dependency_graph['123abc'])

    def test_create_mermaid_graph(self):
        # Пример данных графа
        dependency_graph = {
            '123abc': ['file_2.txt', 'file_1.txt']
        }

        # Вызовем функцию для создания графа
        mermaid_graph = create_mermaid_graph(dependency_graph)

        # Проверим, что граф создан корректно
        self.assertIn("graph TD", mermaid_graph)
        self.assertIn("123abc", mermaid_graph)
        self.assertIn("file_2_txt", mermaid_graph)
        self.assertIn("file_1_txt", mermaid_graph)

    @patch('builtins.open', create=True)
    def test_save_graph_to_file(self, mock_open):
        # Мокируем открытие файла для записи
        mock_file = MagicMock()
        mock_open.return_value = mock_file

        # Пример графа
        mermaid_graph = "graph TD\n123abc --> file_2_txt"

        # Вызовем функцию для сохранения графа в файл
        save_graph_to_file(mermaid_graph, "C:/Projects/config_2/output_graph.mmd")

        # Проверим, что файл был записан
        mock_file.write.assert_called_once_with(mermaid_graph)

if __name__ == '__main__':
    unittest.main()
