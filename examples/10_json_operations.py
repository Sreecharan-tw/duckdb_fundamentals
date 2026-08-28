"""
DuckDB JSON Operations
Example 10 demonstrates working with JSON data.
"""

import duckdb
import json

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB JSON Operations")
print("=" * 60)

# Create table with JSON data
print("\n1. Creating table with JSON column...")
conn.execute("""
    CREATE TABLE user_profiles (
        user_id INTEGER,
        username VARCHAR,
        profile JSON
    )
""")

# Insert JSON data
conn.execute("""
    INSERT INTO user_profiles VALUES
    (1, 'alice', '{"name": "Alice Johnson", "age": 30, "city": "New York", "skills": ["Python", "SQL", "AWS"]}'),
    (2, 'bob', '{"name": "Bob Smith", "age": 28, "city": "London", "skills": ["JavaScript", "React", "Node.js"]}'),
    (3, 'charlie', '{"name": "Charlie Davis", "age": 35, "city": "Tokyo", "skills": ["Go", "Rust", "C++"]}'),
    (4, 'diana', '{"name": "Diana Wilson", "age": 26, "city": "Toronto", "skills": ["Python", "ML", "TensorFlow"]}')
""")
print("✓ Table with JSON data created")

# Extract values from JSON
print("\n2. Extracting values from JSON...")
result = conn.execute("""
    SELECT
        username,
        profile->>'name' as name,
        profile->>'age' as age,
        profile->>'city' as city
    FROM user_profiles
""").fetchall()

print("User profiles extracted:")
print(f"{'Username':<10} {'Name':<20} {'Age':>5} {'City':<15}")
print("-" * 55)
for username, name, age, city in result:
    print(f"{username:<10} {name:<20} {age:>5} {city:<15}")

# Access array elements in JSON
print("\n3. Accessing JSON arrays...")
result = conn.execute("""
    SELECT
        username,
        profile->>'name' as name,
        profile->'skills'->[0] as first_skill,
        profile->'skills'->[1] as second_skill,
        json_array_length(profile->'skills') as num_skills
    FROM user_profiles
""").fetchall()

print("User skills:")
print(f"{'Username':<10} {'Name':<20} {'Skill 1':<15} {'Skill 2':<15} {'Total':>5}")
print("-" * 70)
for username, name, skill1, skill2, num_skills in result:
    skill1_str = str(skill1).strip('"') if skill1 else ''
    skill2_str = str(skill2).strip('"') if skill2 else ''
    print(f"{username:<10} {name:<20} {skill1_str:<15} {skill2_str:<15} {num_skills:>5}")

# JSON functions
print("\n4. JSON utility functions...")
result = conn.execute("""
    SELECT
        username,
        json_keys(profile) as all_keys,
        json_type(profile) as json_type,
        json_valid(profile) as is_valid_json
    FROM user_profiles
    LIMIT 2
""").fetchall()

for username, keys, jtype, valid in result:
    print(f"  {username}: keys={keys}, type={jtype}, valid={valid}")

# Extract with type casting
print("\n5. Extracting and casting JSON values...")
result = conn.execute("""
    SELECT
        username,
        CAST(profile->>'age' AS INTEGER) as age,
        CAST(json_array_length(profile->'skills') AS INTEGER) as num_skills,
        CASE
            WHEN CAST(profile->>'age' AS INTEGER) < 30 THEN 'Junior'
            ELSE 'Senior'
        END as career_level
    FROM user_profiles
    ORDER BY age
""").fetchall()

print("Age-based categorization:")
for username, age, num_skills, level in result:
    print(f"  {username}: age {age}, {num_skills} skills, {level}")

# Create table from JSON extraction
print("\n6. Creating normalized table from JSON...")
conn.execute("""
    CREATE TABLE user_details AS
    SELECT
        user_id,
        username,
        profile->>'name' as name,
        CAST(profile->>'age' AS INTEGER) as age,
        profile->>'city' as city
    FROM user_profiles
""")

result = conn.execute("SELECT * FROM user_details").fetchall()
print("Normalized user details:")
for user_id, username, name, age, city in result:
    print(f"  {user_id}. {name} ({username}), age {age} in {city}")

# Working with JSON arrays
print("\n7. Unnesting JSON arrays...")
conn.execute("""
    CREATE TABLE user_skills AS
    SELECT
        user_id,
        username,
        unnest(json_extract_array(profile, '$.skills')) as skill
    FROM user_profiles
""")

result = conn.execute("""
    SELECT
        user_id,
        username,
        skill,
        skill as skill_clean
    FROM user_skills
    ORDER BY user_id, skill
""").fetchall()

print("User skills (unnested):")
for user_id, username, skill, _ in result:
    skill_clean = str(skill).strip('"')
    print(f"  {user_id}. {username}: {skill_clean}")

# Aggregate JSON
print("\n8. Aggregating skills by user...")
result = conn.execute("""
    SELECT
        user_id,
        username,
        COUNT(skill) as num_skills,
        STRING_AGG(skill, ', ') as all_skills
    FROM user_skills
    GROUP BY user_id, username
    ORDER BY num_skills DESC
""").fetchall()

print("Skills summary:")
for user_id, username, num_skills, all_skills in result:
    all_skills_clean = all_skills.replace('"', '')
    print(f"  {username}: {num_skills} skills - {all_skills_clean}")

# Build JSON from query results
print("\n9. Building JSON from query results...")
result = conn.execute("""
    SELECT
        user_id,
        username,
        json_object(
            'name', profile->>'name',
            'age', profile->>'age',
            'city', profile->>'city',
            'skill_count', json_array_length(profile->'skills')
        ) as summary
    FROM user_profiles
    LIMIT 2
""").fetchall()

print("Rebuilt JSON summaries:")
for user_id, username, summary in result:
    print(f"  {username}: {summary}")

# Query nested JSON structures
print("\n10. Complex JSON queries...")

# Create more complex JSON data
conn.execute("""
    CREATE TABLE projects AS
    SELECT 1 as project_id, 'Project A' as name,
    '{"team": {"lead": "Alice", "size": 5}, "budget": {"total": 100000, "spent": 75000}}'::JSON as data
    UNION ALL
    SELECT 2, 'Project B',
    '{"team": {"lead": "Bob", "size": 3}, "budget": {"total": 50000, "spent": 45000}}'::JSON
    UNION ALL
    SELECT 3, 'Project C',
    '{"team": {"lead": "Charlie", "size": 8}, "budget": {"total": 150000, "spent": 120000}}'::JSON
""")

result = conn.execute("""
    SELECT
        name,
        data->'team'->>'lead' as team_lead,
        CAST(data->'team'->>'size' AS INTEGER) as team_size,
        CAST(data->'budget'->>'total' AS DECIMAL) as total_budget,
        CAST(data->'budget'->>'spent' AS DECIMAL) as spent,
        CAST(data->'budget'->>'total' AS DECIMAL) - CAST(data->'budget'->>'spent' AS DECIMAL) as remaining
    FROM projects
""").fetchall()

print("Project details from JSON:")
print(f"{'Project':<15} {'Lead':<12} {'Team':>5} {'Budget':>12} {'Spent':>12} {'Remaining':>12}")
print("-" * 70)
for name, lead, team_size, budget, spent, remaining in result:
    print(f"{name:<15} {lead:<12} {team_size:>5} ${budget:>11.0f} ${spent:>11.0f} ${remaining:>11.0f}")

print("\n" + "=" * 60)
print("JSON operations complete!")
print("=" * 60)
