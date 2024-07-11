import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def aggregate_experience(data):
    skills_duration = {}
    for jobs in data.values():
        for job in jobs:
            duration = job['duration_months']
            for skill in job['skills']:
                clean_skill = skill.split(':')[-1].strip()  # Clean "Skills:" prefix
                if clean_skill in skills_duration:
                    skills_duration[clean_skill] += duration
                else:
                    skills_duration[clean_skill] = duration
    return sorted(skills_duration.items(), key=lambda x: x[1], reverse=True)

def parse_categories(settings):
    categories = {}
    for category, skill_groups in settings.items():
        for skill_group in skill_groups:
            for skill in skill_group['skills']:
                categories[skill.lower()] = category
    return categories

def get_skill_category(categories, skill):
    return categories.get(skill.lower(), "Uncategorized")

def add_categories_to_experience(exp_list, categories):
    for exp in exp_list:
        exp['Category'] = get_skill_category(categories, exp['Skill'])
    return exp_list

def get_skill_grade(category, duration):
    grade_scale = {'Programming': 3, 'Tools': 4, 'default': 3}
    scale = grade_scale.get(category, grade_scale['default'])
    grade = (duration // 12) * scale
    return min(grade, 9)

def add_skill_grades(exp_list):
    for exp in exp_list:
        exp['Grade'] = get_skill_grade(exp['Category'], exp['Duration'])
    return exp_list

def sort_experience_by_category(exp_list):
    return sorted(exp_list, key=lambda x: (x['Category'], -x['Duration']))

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    profile_path = '../files/linkedin_experience.json'
    settings_path = '../files/skill_category.json'
    output_path = '..//files/view_experience.json'

    profile_data = load_json(profile_path)
    settings_data = load_json(settings_path)
    
    experience_list = aggregate_experience(profile_data)
    categories = parse_categories(settings_data)
    
    experience_list = [{'Skill': skill, 'Duration': duration} for skill, duration in experience_list]
    experience_list = add_categories_to_experience(experience_list, categories)
    experience_list = add_skill_grades(experience_list)
    experience_list = sort_experience_by_category(experience_list)
    
    save_json(experience_list, output_path)

if __name__ == "__main__":
    main()
