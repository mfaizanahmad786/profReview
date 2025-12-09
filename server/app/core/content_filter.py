"""
Content Moderation Module
Filters profanity in English (using better-profanity) and Roman Urdu (custom list)
"""

from better_profanity import profanity
import re
from typing import Tuple

# Initialize better-profanity for English
profanity.load_censor_words()

# Comprehensive Roman Urdu profanity list
# Organized by severity
URDU_PROFANITY_SEVERE = [
    # Extremely offensive - immediate block
    'harami', 'haramzada', 'haramzadi', 'haramkhor',
    'bhenchod', 'behenchod', 'behen chod', 'madarchod',
    'madar chod', 'gandu', 'gaandu', 'randi', 'randwa',
    'bhadwa', 'bhadwe', 'chutiya', 'chutiye', 'lund',
    'lavde', 'dalle', 'kanjar', 'kanjari', 'kamini',
]

URDU_PROFANITY_MODERATE = [
    # Insulting/offensive
    'kamina', 'kameena', 'kaminay', 'kameenay',
    'nalayak', 'nalaik', 'nalaiq', 'nalayiq',
    'kutta', 'kutte', 'kuttay', 'kutti',
    'gadha', 'gadhe', 'gadhay', 'gadhi',
    'badtameez', 'badtamiz', 'beghairat', 'bay-ghairat',
    'ghaleez', 'ghaliz', 'neech', 'zaleel',
    'begherat', 'bay ghairat', 'besharam', 'bay-sharam',
    'saala', 'sala', 'sali', 'saale', 'saali',
]

URDU_PROFANITY_MILD = [
    # Mild insults
    'bewakoof', 'bewaqoof', 'be-waqoof', 'bevakoof',
    'pagal', 'paagal', 'pagla', 'pagli',
    'ullu', 'ulloo', 'buddhu', 'budhu',
    'ganda', 'ghanda', 'kharab', 'kharabi',
    'chaawal', 'chawal', 'vella', 'vela',
    'jahil', 'jahel', 'gawaar', 'gawar',
]

# Compound phrases (more context-specific)
URDU_PHRASES = [
    'ullu ka pattha', 'ullu ka patha', 'ullu ke pathe',
    'gandi harkat', 'gandi harkaten', 'gandi baat',
    'kharab aadmi', 'bura aadmi', 'bura banda',
    'maa ki', 'baap ki', 'bhen ki',
]

# Combine all lists
ALL_URDU_PROFANITY = (
    URDU_PROFANITY_SEVERE + 
    URDU_PROFANITY_MODERATE + 
    URDU_PROFANITY_MILD +
    URDU_PHRASES
)

# Add Roman Urdu words to better-profanity's list
profanity.add_censor_words(ALL_URDU_PROFANITY)


def create_flexible_pattern(word: str) -> str:
    """
    Create regex pattern that handles spelling variations
    Examples:
    - 'kamina' matches 'kamina', 'kameena', 'kaminah'
    - 'bewakoof' matches 'bewakoof', 'bewaqoof', 'be-waqoof'
    """
    # Replace common variations
    pattern = word
    pattern = pattern.replace('a', '[aä@]')
    pattern = pattern.replace('e', '[eē3]')
    pattern = pattern.replace('i', '[iī1!]')
    pattern = pattern.replace('o', '[oō0]')
    pattern = pattern.replace('u', '[uū]')
    pattern = pattern.replace('q', '[qk]')
    pattern = pattern.replace('k', '[kq]')
    
    # Handle optional spacing and hyphens
    pattern = pattern.replace(' ', r'[\s\-_]*')
    
    # Word boundaries
    pattern = r'\b' + pattern + r's?\b'  # Optional plural 's'
    
    return pattern


# Pre-compile regex patterns for performance
URDU_PATTERNS = [
    re.compile(create_flexible_pattern(word), re.IGNORECASE)
    for word in ALL_URDU_PROFANITY
]


def contains_profanity(text: str) -> Tuple[bool, str]:
    """
    Check if text contains profanity in English or Roman Urdu
    
    Args:
        text: The text to check
        
    Returns:
        Tuple of (is_profane, reason)
        - is_profane: True if profanity detected
        - reason: Description of what was found
    """
    if not text or len(text.strip()) < 2:
        return False, ""
    
    # Check using better-profanity (handles English + our added Urdu words)
    if profanity.contains_profanity(text):
        censored = profanity.censor(text)
        return True, "inappropriate language detected"
    
    # Additional check with regex patterns for variations
    text_lower = text.lower()
    for pattern in URDU_PATTERNS:
        if pattern.search(text_lower):
            return True, "inappropriate language detected"
    
    return False, ""


def censor_text(text: str) -> str:
    """
    Replace profanity with asterisks
    
    Args:
        text: The text to censor
        
    Returns:
        Censored text with profanity replaced by asterisks
    """
    if not text:
        return text
    
    # Use better-profanity's censoring
    censored = profanity.censor(text)
    
    # Additional censoring for regex patterns
    for pattern in URDU_PATTERNS:
        censored = pattern.sub(lambda m: '*' * len(m.group()), censored)
    
    return censored


def get_severity_level(text: str) -> str:
    """
    Determine severity of profanity found
    
    Returns: 'severe', 'moderate', 'mild', or 'none'
    """
    if not text:
        return 'none'
    
    text_lower = text.lower()
    
    # Check severe words
    for word in URDU_PROFANITY_SEVERE:
        if word in text_lower:
            return 'severe'
    
    # Check moderate words
    for word in URDU_PROFANITY_MODERATE:
        if word in text_lower:
            return 'moderate'
    
    # Check mild words
    for word in URDU_PROFANITY_MILD:
        if word in text_lower:
            return 'mild'
    
    return 'none'


# For testing/debugging
def test_filter():
    """Test the profanity filter with sample texts"""
    test_cases = [
        "This is a great professor",
        "He is a kamina person",
        "What a bewakoof explanation",
        "This damn professor is annoying",
        "Ye harami teacher hai",
        "Very good teaching style",
    ]
    
    print("Testing Content Filter:\n")
    for text in test_cases:
        is_profane, reason = contains_profanity(text)
        severity = get_severity_level(text)
        censored = censor_text(text)
        
        print(f"Text: {text}")
        print(f"  Profane: {is_profane}")
        print(f"  Severity: {severity}")
        print(f"  Censored: {censored}")
        print()


if __name__ == "__main__":
    test_filter()
