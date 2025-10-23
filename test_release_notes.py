#!/usr/bin/env python3
"""
Unit tests for the release notes generator.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_release_notes import OctopusReleaseNotesGenerator


class TestOctopusReleaseNotesGenerator(unittest.TestCase):
    """Test the OctopusReleaseNotesGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = OctopusReleaseNotesGenerator(
            octopus_url="https://octopus.example.com",
            octopus_api_key="API-TEST123",
            github_token="ghp_test123"
        )
    
    def test_parse_github_url_valid(self):
        """Test parsing a valid GitHub URL."""
        url = "https://github.com/owner/repo/commit/abc123"
        owner, repo = self.generator.parse_github_url(url)
        self.assertEqual(owner, "owner")
        self.assertEqual(repo, "repo")
    
    def test_parse_github_url_invalid(self):
        """Test parsing an invalid GitHub URL."""
        url = "https://example.com/not/github"
        owner, repo = self.generator.parse_github_url(url)
        self.assertIsNone(owner)
        self.assertIsNone(repo)
    
    def test_extract_commits_from_build_info_empty(self):
        """Test extracting commits from empty build info."""
        build_info_list = []
        commits = self.generator.extract_commits_from_build_info(build_info_list)
        self.assertEqual(commits, [])
    
    def test_extract_commits_from_build_info_with_commits(self):
        """Test extracting commits from build info with commits."""
        build_info_list = [
            {
                'Commits': [
                    {
                        'Id': 'abc123',
                        'Comment': 'Test commit',
                        'LinkUrl': 'https://github.com/owner/repo/commit/abc123'
                    }
                ]
            }
        ]
        commits = self.generator.extract_commits_from_build_info(build_info_list)
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]['id'], 'abc123')
        self.assertEqual(commits[0]['comment'], 'Test commit')
    
    @patch('generate_release_notes.requests.get')
    def test_get_space_id(self, mock_get):
        """Test getting space ID."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'Id': 'Spaces-1', 'Name': 'Default'},
            {'Id': 'Spaces-2', 'Name': 'Test Space'}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        space_id = self.generator.get_space_id('Test Space')
        self.assertEqual(space_id, 'Spaces-2')
    
    @patch('generate_release_notes.requests.get')
    def test_get_space_id_not_found(self, mock_get):
        """Test getting space ID that doesn't exist."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'Id': 'Spaces-1', 'Name': 'Default'}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            self.generator.get_space_id('Nonexistent Space')
        
        self.assertIn("not found", str(context.exception))
    
    @patch('generate_release_notes.requests.get')
    def test_get_project_id(self, mock_get):
        """Test getting project ID."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'Id': 'Projects-1', 'Name': 'Project A'},
            {'Id': 'Projects-2', 'Name': 'Project B'}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        project_id = self.generator.get_project_id('Spaces-1', 'Project B')
        self.assertEqual(project_id, 'Projects-2')
    
    @patch('generate_release_notes.requests.get')
    def test_get_environment_id(self, mock_get):
        """Test getting environment ID."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'Id': 'Environments-1', 'Name': 'Development'},
            {'Id': 'Environments-2', 'Name': 'Production'}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        env_id = self.generator.get_environment_id('Spaces-1', 'Production')
        self.assertEqual(env_id, 'Environments-2')


class TestReleaseNotesGeneration(unittest.TestCase):
    """Test release notes generation."""
    
    @patch('generate_release_notes.requests.get')
    def test_generate_release_notes_no_commits(self, mock_get):
        """Test generating release notes with no commits."""
        generator = OctopusReleaseNotesGenerator(
            octopus_url="https://octopus.example.com",
            octopus_api_key="API-TEST123"
        )
        
        # Mock responses
        mock_responses = [
            # Spaces
            Mock(json=lambda: [{'Id': 'Spaces-1', 'Name': 'Test Space'}]),
            # Projects
            Mock(json=lambda: [{'Id': 'Projects-1', 'Name': 'Test Project'}]),
            # Environments
            Mock(json=lambda: [{'Id': 'Environments-1', 'Name': 'Production'}]),
            # Deployments
            Mock(json=lambda: {'Items': [{'ReleaseId': 'Releases-1', 'Created': '2025-10-23T10:00:00Z'}]}),
            # Release
            Mock(json=lambda: {'Id': 'Releases-1', 'Version': '1.0.0', 'BuildInformation': []}),
        ]
        
        for mock_resp in mock_responses:
            mock_resp.raise_for_status = Mock()
        
        mock_get.side_effect = mock_responses
        
        notes = generator.generate_release_notes('Test Space', 'Test Project', 'Production')
        
        self.assertIn('Release Notes: 1.0.0', notes)
        self.assertIn('Test Project', notes)
        self.assertIn('Production', notes)
        self.assertIn('No commit information available', notes)


if __name__ == '__main__':
    unittest.main()
