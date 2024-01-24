# School Information Database Schema

This repo uses SQLAlchemy ORM to define and interact with a PostgreSQL database for storing detailed information about schools, including their locations, financials, control characteristics, and admissions data.

## Database Schema

The database consists of the following tables:

### `School`

- Represents basic information about each school.
- Columns:
  - `id` (Integer, Primary Key)
  - `name` (String)
  - `unitid` (Integer, Unique)
  - `url` (String)
- Relationships:
  - Has many `Location`
  - Has many `Finance`
  - Has many `Control`
  - Has many `Admission`

### `Location`

- Stores location details for each school.
- Columns:
  - `id` (Integer, Primary Key)
  - `school_id` (Integer, Foreign Key to `School`)
  - `city` (String, Not Null)
  - `zipcode` (String, Not Null)
  - `state` (String, Not Null)
  - `region` (String, Not Null)
  - `locale` (String)
- Relationship:
  - Belongs to `School`

### `Finance`

- Contains financial information related to each school.
- Columns:
  - `id` (Integer, Primary Key)
  - `school_id` (Integer, Foreign Key to `School`)
  - `year` (Date)
  - `cost_attendance` (Float)
  - `in_state_tuition` (Float)
  - `out_state_tuition` (Float)
  - `tuition_per_fte` (Float)
  - `instructional_expenditure_per_fte` (Float)
  - `avg_faculty_salary` (Float)
- Relationship:
  - Belongs to `School`

### `Control`

- Describes control characteristics of each school.
- Columns:
  - `id` (Integer, Primary Key)
  - `school_id` (Integer, Foreign Key to `School`)
  - `under_investigation` (Boolean)
  - `predominant_deg` (String)
  - `highest_deg` (String)
  - `control` (String)
  - `hbcu` (Boolean)
  - `religious_affiliation` (String)
  - `carnegie_undergrad` (String)
  - `carnegie_size` (String)
- Relationship:
  - Belongs to `School`

### `Admission`

- Stores admissions data for each school.
- Columns:
  - `id` (Integer, Primary Key)
  - `school_id` (Integer, Foreign Key to `School`)
  - `year` (Date)
  - `admission_rate` (Float)
  - `sat_math_median` (Float)
  - `sat_reading_median` (Float)
  - `sat_writing_median` (Float)
  - `act_math_median` (Float)
  - `act_english_median` (Float)
  - `act_writing_median` (Float)
  - `act_cumulative_median` (Float)
- Relationship:
  - Belongs to `School`

## Usage Examples

### Creating a New School Entry

```python
new_school = School(name='Example University', unitid=12345, url='http://www.example.edu')
session.add(new_school)
session.commit()
```

### Adding Location Information for a School

```python
new_location = Location(school_id=new_school.id, city='Example City', zipcode='12345', state='XY', region='Northeast', locale='Urban')
session.add(new_location)
session.commit()
```

### Querying Schools with Specific Criteria

```python
schools_in_northeast = session.query(School).join(Location).filter(Location.region == 'Northeast').all()
for school in schools_in_northeast:
    print(school.name)
```

### Setup and Configuration

- Ensure you have SQLAlchemy installed: pip install sqlalchemy
- Set up a PostgreSQL database and update the connection string accordingly.
- Run Base.metadata.create_all(engine) to create the tables.
