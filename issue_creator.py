"""
GitHub issue creation with AI-powered parsing
"""
import asyncio
import logging
import os
from typing import Dict, Any, Optional
import aiohttp
import json

logger = logging.getLogger(__name__)

class IssueCreator:
    """Creates GitHub issues from voice transcriptions using AI parsing"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN') or os.getenv('GH_PAT')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.github_api_base = 'https://api.github.com'
        
        if not self.github_token:
            raise ValueError("GitHub token not found. Set GITHUB_TOKEN or GH_PAT environment variable.")
    
    async def create_issue(self, repository: str, voice_text: str, context: str = "") -> Dict[str, Any]:
        """
        Create a GitHub issue from voice transcription
        
        Args:
            repository: GitHub repository in format 'owner/repo'
            voice_text: Transcribed voice content
            context: Additional context for the issue
            
        Returns:
            GitHub issue data
        """
        try:
            # Parse the voice text into structured issue data
            issue_data = await self._parse_voice_to_issue(voice_text, context)
            
            # Create the GitHub issue
            github_issue = await self._create_github_issue(repository, issue_data)
            
            logger.info(f"Created issue #{github_issue['number']} in {repository}")
            return github_issue
            
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            raise
    
    async def _parse_voice_to_issue(self, voice_text: str, context: str) -> Dict[str, str]:
        """Parse voice transcription into GitHub issue format using AI"""
        
        if self.anthropic_api_key:
            return await self._parse_with_ai(voice_text, context)
        else:
            return self._parse_with_heuristics(voice_text, context)
    
    async def _parse_with_ai(self, voice_text: str, context: str) -> Dict[str, str]:
        """Use Claude AI to parse voice text into issue structure"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Content-Type': 'application/json',
                    'x-api-key': self.anthropic_api_key,
                    'anthropic-version': '2023-06-01'
                }
                
                prompt = f"""Please analyze this voice transcription and convert it into a well-structured GitHub issue:

Voice transcription: "{voice_text}"

Additional context: "{context}"

Please provide a JSON response with:
- title: A clear, concise issue title (under 80 characters)
- body: A detailed issue description with proper formatting
- labels: An array of relevant labels (like 'bug', 'feature', 'enhancement', etc.)

Format the body with proper markdown including:
- Clear problem description or feature request
- Steps to reproduce (if it's a bug)
- Expected vs actual behavior (if applicable)
- Acceptance criteria or requirements

Make sure the response is valid JSON."""

                data = {
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
                
                async with session.post(
                    'https://api.anthropic.com/v1/messages',
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['content'][0]['text']
                        
                        try:
                            # Extract JSON from the response
                            json_start = content.find('{')
                            json_end = content.rfind('}') + 1
                            json_str = content[json_start:json_end]
                            parsed_data = json.loads(json_str)
                            
                            return {
                                'title': parsed_data.get('title', 'Voice-generated Issue'),
                                'body': parsed_data.get('body', voice_text),
                                'labels': parsed_data.get('labels', ['voice-generated'])
                            }
                        except json.JSONDecodeError:
                            logger.warning("Could not parse AI response as JSON, using fallback")
                            return self._parse_with_heuristics(voice_text, context)
                    else:
                        logger.warning(f"AI API request failed: {response.status}")
                        return self._parse_with_heuristics(voice_text, context)
                        
        except Exception as e:
            logger.error(f"Error calling AI API: {e}")
            return self._parse_with_heuristics(voice_text, context)
    
    def _parse_with_heuristics(self, voice_text: str, context: str) -> Dict[str, str]:
        """Fallback parsing using simple heuristics"""
        
        # Determine if it's likely a bug report or feature request
        bug_keywords = ['bug', 'error', 'broken', 'issue', 'problem', 'not working', 'crash', 'fail']
        feature_keywords = ['feature', 'add', 'new', 'implement', 'create', 'need', 'want', 'should']
        
        text_lower = voice_text.lower()
        is_bug = any(keyword in text_lower for keyword in bug_keywords)
        is_feature = any(keyword in text_lower for keyword in feature_keywords)
        
        # Generate title
        words = voice_text.split()
        title_words = words[:12]  # First 12 words
        title = ' '.join(title_words)
        if len(title) > 80:
            title = title[:77] + '...'
        
        # Add prefix based on type
        if is_bug:
            title = f"Bug: {title}"
            labels = ['bug', 'voice-generated']
        elif is_feature:
            title = f"Feature: {title}"
            labels = ['enhancement', 'voice-generated']
        else:
            title = f"Issue: {title}"
            labels = ['voice-generated']
        
        # Create body
        body = f"""## Voice Transcription

{voice_text}

"""
        
        if context.strip():
            body += f"""## Additional Context

{context}

"""
        
        body += """## Generated Information

This issue was automatically generated from a voice recording.

---
*Created with voice-to-issue tool*"""
        
        return {
            'title': title,
            'body': body,
            'labels': labels
        }
    
    async def _create_github_issue(self, repository: str, issue_data: Dict[str, str]) -> Dict[str, Any]:
        """Create the actual GitHub issue"""
        url = f"{self.github_api_base}/repos/{repository}/issues"
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'title': issue_data['title'],
            'body': issue_data['body'],
            'labels': issue_data.get('labels', [])
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to create GitHub issue: {response.status} - {error_text}")
