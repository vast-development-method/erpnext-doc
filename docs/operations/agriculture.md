# Crop cycles, farm projects and field observations

A crop definition describes repeatable work. A crop cycle places that work on named land and dates. A field observation records what was measured at a particular place and time. A material issue, harvest receipt or employee time entry records an economic event against the project. Creating a cycle authorises its schedule. Stock and accounting effects require their own submitted transactions.

## The crop plan and its project

| Business record | Required relationships and decisions |
|---|---|
| Crop definition | A unique title and crop name identify the plan. Store species, life-cycle classification, optional target warehouse, plant and row spacing with units, planting area and yield unit. Materials required, expected produce and by-products are separate component lists. |
| Crop task | The crop owns ordered task rows. Each has a name, first and last day, priority and holiday handling selection. First day must be no later than last day. Sort by first day, preserving the relative order of rows that start together. |
| Crop cycle | A unique cycle title, a crop and a start date identify the planting. The cycle owns land references, disease detections and links to selected observations. Missing plant-spacing and row-spacing units inherit the corresponding crop units independently. |
| Project and task | On cycle creation, create a project named for the cycle and attach it to the cycle. Each crop task creates a project task with its subject, priority, project and dated start and end. Editing the cycle to add disease observations invokes a separate treatment scheduling decision. |
| Disease detection | Each cycle detection records its disease, detection start date and whether its treatment tasks were created. Disease definitions supply their own list of task names, offsets and priorities. A subsequent detection of the same disease has its own row and scheduling state. |

Let $P$ be the greater of the configured crop period and the largest task end day. Project end equals cycle start plus $P-1$ calendar days. Each task begins on start plus its first-day offset minus one and ends on start plus its last-day offset minus one. Disease tasks use the detection start in place of cycle start. The generated task dates use calendar offsets even where the task template records a holiday preference.

For a crop configured for ten days with task bounds 2–4 and 9–12, the effective period becomes twelve days. A cycle starting 1 April ends on 12 April. The first task spans 2–4 April inclusive. A disease detected on 6 April with a treatment on day three creates a task for 8 April on the same project. Reopening or saving the cycle after the detection was marked as scheduled does not generate those treatment tasks again.

## Sampling and land association

An analysis criterion has a unique title and an analytical subject such as soil, soil texture, water, fertiliser, plant or weather. Selecting the criteria for a measurement appends the definitions for that subject. A measurement belongs to its recorded collection point and observation time. Criteria rows keep reading and permissible limits when present. Recording a result does not post an inventory issue or place a purchase order.

The water sample maintains three ordered instants. Collection must be on or before laboratory testing. Testing must be on or before the result. When the result time is absent during date completion, it takes the testing time. Equality is permitted. The water sample also records origin, container, temperature at collection and storage, appearance and responsible person. These facts belong to that sample even if the site description subsequently changes.

For a crop cycle, refresh linked soil texture, soil and plant analyses by testing the collection point against the exterior ring of each attached land polygon. A horizontal ray that crosses an odd number of ring edges identifies an interior point. The same point within two selected plots contributes its analysis once per refresh. Refresh appends selected links and removes duplicates within that selection. It does not establish uniqueness against rows saved on an earlier refresh. Use the observation identity when aggregating underlying results. An analysis belongs to a cycle through the location relationship, not through a global match on crop name. The location search does not apply a cycle date cutoff.

## Soil composition classification

Store clay, sand and silt as percentages. On an edit the least recently edited component can be balanced to 100 minus the integer portions of the two other components. Validate each final component in the inclusive interval 0 to 100 and require their sum to equal 100. Preserve the recorded percentages separately from the resulting class. In the ordered decisions below, $C$, $A$ and $S$ represent clay, sand and silt percentages respectively. Choose the **first** true row. This is the classification used by the record.

| Condition, in priority order | Class |
|---|---|
| $S+1.5C<15$ | Sand |
| $S+1.5C\ge15$ and $S+2C<30$ | Loamy sand |
| $7\le C<20$, or $A>52$ and $S+2C\ge30$, or $C<7$ and $S<50$ and $S+2C\ge30$ | Sandy loam |
| $7\le C<27$, $28\le S<50$ and $A\le52$ | Loam |
| $S\ge50$ and $12\le C<27$, or $50\le S<80$ and $C<12$ | Silt loam |
| $S\ge80$ and $C<12$ | Silt |
| $20\le C<35$, $S<28$ and $A>45$ | Sandy clay loam |
| $27\le C<40$ and $20<A\le45$ | Clay loam |
| $27\le C<40$ and $A\le20$ | Silty clay loam |
| $C\ge35$ and $A>45$ | Sandy clay |
| $C\ge40$ and $S\ge40$ | Silty clay |
| $C\ge40$, $A\le45$ and $S<40$ | Clay |
| No row matches | Leave the class for selection |

For 10% clay, 40% sand and 50% silt the first matching row yields sandy loam. With 25% clay, 40% sand and 35% silt the result is loam. This ordering matters when a sample satisfies more than one expression.

## Access and cost attribution

Farm managers may create and delete the principal crop, cycle and analysis records. Farm users have read and change rights on these record families and may use their granted report, print, export and sharing functions. A child measurement uses the parent observation's access decision. A generated project and its work, stock and accounting records use their own permissions. A crop material row can propose the product's stock unit and valuation rate. The financial balance of the crop project comes from actual project-linked issues, services and time. Planned input rates, field readings and possible yield are separate measures.
