


> Written with richie bao. Created on Sat Oct 31 18:38:28 2020
# 参数化设计方法综述与启示（rough draft）

## 相关概念及关系
### 参数化/设计(parametric/ design)
#### grasshopper
As designers, we struggle primarily with interface of the traditional syntax of code/computation. These traditional programming interfaces, such as coding in C# or Fortran, or even scripting in Python, have not yet operated at a level of abstraction designers are accustomed to thinking. Designers have had to rely on a team of computational experts attempting to translate the designer’s language into computer code (scripting). Much can be lost in the translation. However, with developments in GUI (graphic user interfaces) such as Grasshopper software (plug-ins), a huge barrier has been crossed.[1-2] 

As designers, we struggle primarily with interface of the traditional syntax of code/computation. These traditional programming interfaces, such as coding in C# or Fortran, or even scripting in Python, have not yet operated at a level of abstraction designers are accustomed to thinking. Designers have had to rely on a team of computational experts attempting to translate the designer’s language into computer code (scripting). Much can be lost in the translation. However, with developments in GUI (graphic user interfaces) such as Grasshopper software (plug-ins), a huge barrier has been crossed.[1-2]

GUI-based scripting engines such as Grasshopper, Dynamo, Kismet, and Marionette have all become a contemporary phenomenon, opening up new computational vistas to designers who would simply not have bothered to cross the learning barrier to entry in text-based coding editors. [1-2]

These coding and scripting abstraction/ interface platforms have acted as a gateway for many designers, who expanded their reach to numerous problems and data sets in the emerging technological world. Grasshopper, for example, initially launched by McNeel and Associates and created by programmer David Rutten,40 was built upon, after its creation, by numerous add-ons, plug-ins, or extensions (e.g., Rhinoceros). With the built-in script in the background, designers could now engage in parametric design, skipping over the tedious and discouraging scripting, undeterred by the computational demands of the past. Moreover, designers could now concentrate on their work, instead of spending time learning and acquiring computational tools to get to the task. The simplicity with which Grasshopper and Rhino could be utilized led to widespread use of the software across top architectural firms and eventually landscape architecture offices, opening the computational world.41 [1-2]

The success of the software was largely due to Robert McNeel’s insight: “Writing code is not something designers really want to get their head into.” His “business model” had a two-pronged approach: “designers set up sophisticated relationships between the parts of the design problem” and, in addition, the company would make the software available for free during the development process, benefitting from the input of users worldwide.42 Although a small firm by comparison, without the deep pockets of a Dassault Systèmes or Autodesk, by 2009 McNeel reported having 250,000 Rhino users worldwide, among them 50,000 in the field of architecture. This number has since bourgeoned further, as Rhino became commonplace in architectural offices and urban design practices.43[1-2]

In the field of architecture, the virtual wall beyond software and databased design has already been pierced,[1-2]

A new generation of digital natives have been brought up by the new interactive normalcy to live, work, and create abstractly through these virtual media. Machine learning and script definition of software are assisting to fill in the gaps of the executable details of our creative process. The executable interface is now rapidly evolving. It is accessible for designers to “code” problems at the highest levels of abstraction through gesture and real-time feedback, all while designers observe the instantaneous impact of their digital interaction on the built environment.49[1-2]

However, even though the more geometrically “simple” in design and process are easier to calculate through computational design, why do we see this technology being so often only used and advertised in the most abstract or biomorphic of projects? It is certainly refreshing to see these tools used as an enabler or inspiration for complex and new ways of design thinking. However, we must also take advantage of the day-to-day problem-solving capabilities and practical use of such computation engines.[1-2]

We describe, perhaps in a negative tone, the common perceptions and prevailing uses of Grasshopper and other parametric engines to hopefully draw the reader’s attention to a new platform of thinking about computational design and technology in landscape architecture. Software, such as Grasshopper or Dynamo, must be recognized as problem-solving tools and engines of creativity. These tools are not simply engines of graphic communication that perhaps a new generation of design professionals may have mistakenly interpreted and represented as a means to an end in itself. Rather, parametric tools, such as Grasshopper, are practical instruments with the potential to address problems and find solutions while unleashing a vast source of creativity. For example, graduate students used:[1-2]

Emerging from the most ancient of traditions in design and architecture, our obsession with geometry and form are driven by mathematical relationships that are both discreet and subliminal. Grasshopper, Dynamo, and Python are some of the first conversation openers in computational design today, yet it is specifically their abstraction of and thus accessibility to computation that have driven their remarkable success.[1-2]

Many designers will not engage at the high level of syntactical knowledge necessary for scripting given time constraints as one of significant barriers. However, Grasshopper, Rhino, other GUI-based scripting allows designers to more readily connect the outcome of code with the formal representation without having to know how to write code. [1-2]

The world-renowned architect Bjarke Ingels, in his 2013 interview, “Inside the Business of Design,” described the impact of Grasshopper and visual scripting on architecture in these simple terms: “Grasshopper is to parametric scripting what Windows and Macintosh were to the graphical interface for personal computing.” Ingels describes the essence of GUI-based parametric design as follows: “Scripting came from being this incredibly difficult thing in architecture to, at least, I can understand the principles. You basically construct incredibly complex formulas by graphically combining different variables with little wires almost like a switch board.”53[1-2]

One such example is a set of site analysis plug-in objects built using Vectorworks’s Marionette algorithmic scripting environment. Marionette is not an application but rather a technology stack that brings visual scripting and algorithmic design capability to the Vectorworks CAD and BIM line of applications. While many design professionals are familiar, at least in concept, with the notion of complex 3D models being powered by algorithms—such as with Rhino and Grasshopper—the ability to program specific tools that perform queries on data and spit out actionable information is an excellent example of the rising use of algorithmic design. [1-9]

As such, they are richer instruments to query. Tools such as Grasshopper, Dynamo, Marionette, and others take the query process further in several ways. While they still feature the capacity to be wired to BIM tools and the metadata attached therein, they can be—as seen in the example above—wired to other data outside the realm of the BIM application. These visual scripts on-ramp designers into the world of computer programming, which furthers the nature and capacity for designers to ponder and ask deeper types of questions—questions that can revolutionize our environments, even if just one project at a time. As Daniel Belcher, of Robert McNeel & Associates, says, when asked what skills coding teaches beyond the world of being a software developer, “the understandings of algorithm, process, flow, and logic that underpin the creative act of programming are critical to agency in the modern world.” [1-9]

Today, Grasshopper, a visual programming editor for the 3D modeling software Rhino3D, is the primary tool used by landscape architects for both parametric site analysis and parametric design. Conceived in 2007 by David Rutten at Robert McNeel and Associates,14 15 Grasshopper uses draggable blocks of data and functions (called “components”) connected by wires, thus allowing users who do not know anything about computer programming to use computational logic to manipulate Rhino and generate highly complex 3D models. In landscape architecture, Grasshopper is used in both academic projects and increasingly in professional projects as well. For instance, the firm Fletcher Studio used Grasshopper extensively to simulate conditions and create both conceptual design packages and construction documentation for the $2.8 million renovation of San Francisco’s South Park.16 According to Fletcher Studio’s founder, David Fletcher, “Quite literally everything that is in the plans was generated in Grasshopper at one time.”17[1-12]

Scripted landscapes: code as design too[1-12]

As already discussed, landscape architects are becoming increasingly reliant on parametric design tools such as Grasshopper. As sites have become larger and projects have become more complex, design trends have also shifted further away from the formal, axial landscapes of the early twentieth century into complex, nonorthogonal landscapes with hybridized, flexible programs. To each of these ends, parametric and scripting tools have become huge time-savers. During analysis and conceptual design, these tools allow designers to input environmental and socioeconomic data in various formats and quickly generate design alternatives that have the potential to dynamically adapt to changing conditions.[1-12]

The “parametric landscape” promises more than a method to quickly iterate through options only to settle on a single solution, as Grasshopper is often used today, or to handle the complex data in sets of construction documents, as in the current state of BIM software. The parametric landscape wants to be an open system that self-organizes in order to, with every feedback loop, consistently arrange itself to meet the complex and changing parameters set forth by a landscape architect. In this effort the landscape architect becomes the author of an algorithm rather than designer of a specific, even if flexible, site solution. [1-15]

This work is also beginning to take shape within the design professions. Andrew Heumann developed a Grasshopper plug-in named Human UI that allows users to create an easy-to-use interface that references specific Grasshopper components. Human UI allows clients to take control of specific elements within a digital model and see, in real time, what happens if they increase the height of the building or change the cut and fill balance of a landscape.[1-15]

In studios across professional landscape architecture programs, students download digital elevation models in ArcGIS, create surfaces in Rhino, manipulate those surfaces with Grasshopper “scripts,” and then contour those surfaces at even intervals to create two-dimensional drawings that represent a three-dimensional landscape. This workflow uses extraordinary computational power to create a representational device that has been used for hundreds of years: the contour line. Those same students will then import that surface into a software program, such as MasterCAM, to create tool paths, which in turn will generate NC code for a CNC router to excavate material that creates a physical manifestation of the designed surface, often in an expanded polystyrene material. These workflows result in many steps of unnecessary translation.[1-15]

[2-4]通篇

2007 saw the introduction of Grasshopper, a new visual scripting plug-in for Rhinoceros. Similar to the popular visual programming language Max/MSP, first introduced in the late 1980s, functional components are represented as graphic nodes and are directionally wired together to create an algorithmic logic. The architectural community was ready for an algorithmic design tool, so Grasshopper rapidly gained in popularity.[2-4]

* case

Aerial view of
South Park, San
Francisco,
California

The initial design for the park was developed through iterative analog diagramming, which was then replicated and expanded with the use of parametric software.[1-5]

In the initial design phase, these decisions were made through intuitive understanding of the parameters of the site and embedded in an analog rule set that guided design decisions. In further research we have codified the relationship between the spatial logics of the design and the material logics of the tectonic, in a parametric algorithm. [1-5]

Initial research was performed in preparation for the Acadia 2014 exhibition, an annual parametric design conference. The central question was: could the design process, the distribution of points and pathways with a distinct tectonic, be replicated? Further, could other contextual influences and conditions be added, and could the tectonic respond to those conditions? Is the use of responsive parametric definitions scalable and can it be applied to larger linear landscapes such as waterfronts, urbanized rivers, etc.? Grasshopper, a parametric plug-in for the 3D modeling program Rhinoceros, was used to further develop the research. FIGURE 1.3.2 Landscape components and site performance diagrams By implementing the design variables into a parametric system, we intended to utilize the system to display the design resiliency of the tectonic and spatial systems. The decision to codify the analog system, developed in the initial phase of design, was driven by the knowledge that future specification of the design in permitting, coordination, and construction documentation would require multiple iterations responding to new constraints and conditions, as they might arise. [1-5]

Grasshopper was further used, to produce the technical documentation for project construction and permitting. A responsive 3D model was prepared, which integrated the site data, including existing utilities and topography. This model was responsive, in the sense that modifications to simple referenced forms would result in universal modifications throughout the master project model. [1-5]

Grasshopper would convert into the modular tablet paver field. This allowed for the clean export of vectors to 2D CAD with minimal trimming and cleanup.[1-5]

With over 18 feet of grade change on the site, and tight tolerances to achieve and accessible public space, Grasshopper again proved to be a powerful ally.[1-5]

Grasshopper was then used to generate a responsive model for the custom play structure. Like the analog pinboard, this model allowed us to quickly generate multiple versions of the structure. The model would automatically distribute netting, fittings, and play elements, responding to the manipulation of the perimeter and interior tube forms. Running component lists could be generated and output to spreadsheets for cost control and evaluation. Final visualizations of the various iterations could be generated at any time, for community design meetings. [1-5]

typically achieved with pen and paper. It also can lead to unanticipated outcomes. A parametric program can allow for the generation of infinite iterations, some of which may never have been conceived. At times, mistakes made in data entry can lead a designer onto a new path of exploration. Yet it is still up to the designer to make the final call in selecting what is worth further developent. Great design often comes from challenging rules and conventions, from responding to insurmountable constraints with solutions. It also comes from human intellect and experience. Memory, experience, emotion, and humor are not yet parameters that can be input into a parametric definition.[1-5]

#### dynamo
BA: When designing computational tools, some strategies we use to ensure our tools are robust and not subject to failure is to try building them as natively as possible. What do I mean when I say that? There has been this HUGE push to open-source tools (which is amazing), but comes with its own set of challenges. As an example, Dynamo is an open-source program to which the industry can contribute its own custom packages, or add-ins. The challenge when using someone else’s open-source package is that you are now subject to the integrity of their tool. If there is a flaw in their tool, or if it no longer works when a new release of Dynamo comes out, you are now subject to that defect. We prefer to use our own custom nodes, as it gives us greater control over the tool and its integrity.
Bill Allen (BA)
Computational Designer
Partner and Director of Building Information[1-3]

A visual scripting environment and online community are now being developed in Dynamo—a plug-in for Revit software for BIM (building information modelling)[2-4]


#### python


### 编程代码(coding/code/codify)
the word “coding” is much more recent; it appeared in the 1950s, when source codes were punched out of cards and then fed into Univac computers that transcribed them into either words or complex binary numerals. The punch cards were not made of waxed tree bark but of cardboard, a derivative of wood, and it is
interesting to note how this original organic link to etched wood prevailed well into the early coding years of the cybernetic age.[1-1]

Using these artificial languages, one can define algorithms – one class of algorithms is those written in computer code.[1-2]

the discussion of “code” as a syntactical language and heuristic process that we push for computational design to become a subject of thought and common language in landscape architecture, to promote new ecological, social, economic, formal, and material design systems in the built environment.[1-2]

However, just as with electronic compilers (translators), in landscape architecture we still struggle with the translation and abstraction of thought processes to machine language.[1-2]

Not all landscape architects will become avid coders. However, it is imperative as a profession agitating for creativity, exploration, innovation, and substantial investment in form generation and alteration of the urban realm that we understand and communicate with those shaping the future components of the synthetic urban construct.[1-2] 

Not all landscape architects will become avid coders. However, it is imperative as a profession agitating for creativity, exploration, innovation, and substantial investment in form generation and alteration of the urban realm that we understand and communicate with those shaping the future components of the synthetic urban construct.[1-2]

Coding is a common language of creation, iteration, logic, communication, exploration, and innovation for the twenty-first century. [1-2]

A computer program is not a task that someone who knows how to code goes right into and writes simply because they know the language. The program is dependent on a problem to be solved. A programmer must know the logic and sequence of commands intended to be developed. The code is simply the wording telling the computer what to do. That communication ability is vital. [1-2]

yet these new tools are digitally driven. Knowing the “maker’s language” today— digital tools that are increasingly driven by code—imbues the design professional with capacity beyond design skills that live only in the world of representational systems;[1-9]

Within the discipline of landscape architecture, in both academia and in practice, scripting and coding are increasingly prevalent as tools for analysis, design, and communication. While some forms of scripting and parametric design have worked their way into the mainstream for both analysis and design purposes, most landscape architects do not actually code. However, those who do have used computer programming for a range of innovative applications that have the potential to expand the scope and reach of landscape architecture quite dramatically beyond site design into the realm of community engagement and participation tools, web-based site analysis and mapping platforms, mobile and web apps, video games, and more.[1-12]

### 计算性设计（computational design） 
A brief history of computation in landscape architecture[1-12]

The extraordinary palette of possibilities offered by new computational methods through geographically positioned modeling and its attributes will enable designers to access more readily a broader palette of options, questions, and solutions, responding physically and spatially to the specificity and inherent complexity of a place. This will also enable an entirely new form of ecology to arise and succeed, one that is much more imbedded in the cultural and topographical quality of each place.[1-1]

The foundation of the modern computer was soundly established by a British mathematician and scientist, Alan Turing, in 1937 in his seminal paper on “Computable Numbers.”5 Apple’s Steve Wozniak believed that Turing set the standards for modern computation: in his keynote address to the 2012 Turing Festival, Wozniak said that “Turing came up with what we know about computers today.”6[1-2]

For Turing’s contemporaries, computation, or computing, meant getting as many people as necessary to complete a task in as short a space of time as was possible. The use of a machine to complete human tasks was a new concept of the time, one society still struggles with in new ways in contemporary culture. Much of Turing’s work investigated the potential of what could be computed by machines in place of their human counterparts.8[1-2]

The origins of computation, from our perspective as designers and planners,emerged first in the 1960s with new thought processes in analysis and environmental planning. This approach is perhaps best explained in 1967 in the seminal paper “Design with Nature,” by Ian McHarg, an approach now referred to as “McHargian Analysis.” Mcharg’s explanation of an overlay system for land classification, coupled with much of the work done and courses taught by Carl Steinitz at the Harvard Graduate School of Design, established a basis for the development of modern GIS (geographic information systems).12[1-2]

In 1965, Chicago architect and Harvard Graduate School of Design Architecture alum Howard T. Fisher, created the Harvard Laboratory for Computer Graphics and Spatial Analysis.[1-2]

Fisher further developed GIS, which spun off a number of computer applications and integrated mapping systems, including tools such as SYMAP (Synagraphic Mapping and Analysis Program), with the ability to print contour maps on a line printer.13[1-2]

Fisher’s pioneering ideas, in turn, inspired Jack Dangermond, then research assistant at the lab from 1968 to 1969, to put these ideas to practical use. Dangermond’s start-up company, ESRI (Environmental Systems Research Institute), was founded in 1969, focusing on software for land use analysis.14[1-2]

In the early 1970s, computation in landscape architecture focused primarily on a two-dimensional understanding of data and mapping overlay. It was not until the late 1970s that three-dimensional computation expanded,[1-2]

The first commercially accessible computers for the masses expanded rapidly in the 1980s, and with that hardware expansion software development would soon follow at an ever-increasing rate. In 1982, Autodesk,founded by John Walker, launched its first version of AutoCAD.20 AutoCAD, to this day, is one of the most heavily used programs for detailed design and drafting in landscape architecture and other design and engineering fields. That same year, Dangermond’s ESRI finally launched Arc/INFO, its first commercially available GIS platform. Arc/INFO remains the leader in large-scale planning and analysis work in landscape architecture.21 Both of these tools, from their early creation, have been dominant in their use in the landscape architecture profession for the last 35 years.[1-2]

Only recently have the detailed drafting and 3D world of CAD (computer-aided design) and the analysis and large-scale data platform of GIS truly started to merge in the software approach of “geo-design.” Perhaps popularized through the first geo-design summit in January 2010, the ideas of geodesign codify the challenges in scale and complexity of landscape computing when shifting scales of models are required from regional ecologies, to civic spaces, to the visual presence of the virtual “wild.”22[1-2]

Within the last decade, with the increase of computational efficiency, we find new models that more directly take advantage of the power of computation to build relationships and form new heuristic models in landscape architecture.[1-2]

The coding of the environment implies a classification, the abstraction of physical and environmental phenomena to create a model that may be used for representation, analysis, or simulation. Design models, visual and/or numerical, describe the world and are the essential fodder through which designers develop design solutions. The continual construction, evolution, and maintenance of these models mediates and develops our relationships between the physical and virtual, underlying our assumptions of the physical world.[1-2]

As our world becomes increasingly algorithmic, we must be aware that technological data usage does not simply become a reflection of privatized mobile/social media data mining, which, while a powerful tool and offering exciting new opportunities in urban planning, does have its limitations in data reliability or sample set.[1-2]

As landscape architects have engaged in the previous decades with GIS, geo-design,and mobile data, we have garnished great rewards in being accumulators of some rather large data sets of physical topography, sea-level rise, and socioeconomic distribution. However, the gathering of data (the inventory) and understanding the algorithms controlling, sorting, or processing that information (the analysis) present the next stage of untold value for the potential of social, formal, materialistic, and environmental models that are more synthetic and controlled by the designer’s intent. This is explored in essay 01.04, “Big Data for Small Places.”[1-2]

Landscape architects are already “embracing digital media as a tool with analytic, performative, and representational possibilities.” The computer is no longer the rival.36 In a dramatic shift, the profession is rapidly moving beyond computation as a design representation medium; the tool is now influencing the thinking process of the landscape architect to shape dynamic models for adaptive and responsive landscapes.37[1-2] 

As landscape architects have engaged in the previous decades with GIS, geo-design,and mobile data, we have garnished great rewards in being accumulators of some rather large data sets of physical topography, sea-level rise, and socioeconomic distribution. However, the gathering of data (the inventory) and understanding the algorithms controlling, sorting, or processing that information (the analysis) present the next stage of untold value for the potential of social, formal, materialistic, and environmental models that are more synthetic and controlled by the designer’s intent. This is explored in essay 01.04, “Big Data for Small Places.”[1-2]

Landscape architects are already “embracing digital media as a tool with analytic, performative, and representational possibilities.” The computer is no longer the rival.36 In a dramatic shift, the profession is rapidly moving beyond computation as a design representation medium; the tool is now influencing the thinking process of the landscape architect to shape dynamic models for adaptive and responsive landscapes.37[1-2]

the influence with which computation and the computationally minded will shape our built environment is without question.[1-2]

It may appear that the complexity of the world around us is increasing in the human ability to interact and control our surrounding everyday objects. In reality, we are seeing an increasing translation from mechanical to digital (coded) language within our daily lives.[1-2]

One of the greatest struggles we face, as a design profession, is our attempt to overcome what we perceive to be the limitations of technology and computation. That perception is that computation is “only” a tool kit, only a set of operations. We must understand computation as a way of thinking, as a way of linking our thought process and dynamic environments. This is very different from “computerization.”[1-2]

Computerization is a tool kit of prefabricated software that we accept or use within the bounds of what it allows our landscape to be. What we yearn for as a profession is computation. That concept goes far beyond the tool kit. Computational design is the systematic method for critical thinking that emphasizes thought process and iteration over memorization and duplication. It stresses the linking of ideas, and interaction between the parts of the problem and the solution. [1-2]

Computational thinking combines the powerful orderly process of algorithmic organization with the equally powerful, but more chaotic, process of iterative design. Computational design is a way of approaching all the challenges in the world around you in a more visionary, creative, far-reaching, and organized way that is more likely to succeed. We engage with computational decisions each day whether we realize it or not. In the design field the passage beyond computational skills, and tools, albeit influenced by computer thinking, is a paradigm shift: “Steps away from ‘form making’ and toward ‘form finding.’”58[1-2]

The terms “computational design” and “parametric design” can be defined in many ways. They may bring to mind forms driven by generative algorithms or the ability to design with various types of data sets or simply the use of Building Information Modeling (BIM) software. We can argue that what the fields of computational design and parametric design hold in terms of potential and capability, they lack in clarity and specificity.[1-3]

A designer that is working parametrically may be thought of as someone who is flipping the traditional process, an editor of constraints first, and an empirical designer once the constraints are designed. What this means for practice is often far more interesting and innovative than the complex forms that initiate such projects. Inherent in the computational design process is the ability to quickly explore multiple design iterations throughout a project. This process is sometimes referred to as “optioneering,” in which consultants and collaborators are brought on early in a design in order to help define the project constraints. As design processes and schedules adapt to emergent modeling and analysis workflows, we find opportunities for new models of practice that simultaneously react to, and influence advances in the field of computational design.[1-3]

First and foremost, there is a general evasion of all-encompassing terms such as “computational design” owing to their vague and abstract nature. Since computational design comes in so many shapes and sizes it is best to describe more specifically what is being offered by these individual practices. In some cases, the focus is on efficiency and precision. In other cases, the focus may be more about achieving a particular level of complexity or in realizing a unique aesthetic. Computational design in and of itself does not possess a style or even a process, but rather provides a broad characterization of a way of thinking through design issues and realizing a project by simply incorporating more layers of information.[1-3]

Computation design will increasingly facilitate our understanding of complex urban, social, environmental, and economic sciences. This continual evolution suggests that landscape architects must be adaptive and resilient and possess the skills to address a wide range of issues. As with technology, humans must develop the personal bandwidth to deal with diverse and complex issues.[1-14]

### 参数化（prametric design）
The roots of understanding computational and parametric design do not lie buried beneath complex mathematical formulas or coding syntax. Instead, they reside in the organization of thoughts and a design approach. When designers understand code and computation in this manner, it is possible to then frame design problems through this lens, opening up a dialogue between design intent and computational iteration and generation.[1-2]

What is not as evident is the logic, the thought process, and the utilization of parametric design that have been applied to bring about the complex execution.[1-2]

It was a feedback loop, where the design drove the code, and the code, in turn, reinfluenced the design. 
Benjamin Koren (BK)
Managing Director of ONE TO ONE ONE TO ONE is a computational geometry and digital fabrication consultancy on art and architecture projects, offering services in bespoke geometric computation, precision 3D CAD construction, integrative CAM fabrication and innovative R&D at all scales.[1-3]

parametric modeling will provide predictive models of land cover and the threedimensional form of a city into the future, based upon a range of design parameters. Our analysis of time, as a design parameter, will include the perception and resilience of landscape-based changes through the day, the seasons, year upon year, the centuries, and the millennium.[1-14]

The importance of computation design emphasizes once again the critical importance of STEM (science, technology, engineering, mathematics) education. It also highlights the challenge of fitting this needed knowledge into an already jam-packed curriculum. Undoubtedly, the user interface will increasingly make such tools accessible to a wider range of users, although not every landscape architect will have the interest and aptitude to embrace the mathematical or programming skills necessary for parametric design. [1-14]

Just as many firms have CADD and BIM managers today, one can envision the position of “Director of Parametric Design” within landscape architecture firms, a position that already exists within some product design companies, such as Nike, and a growing number of architecture firms.[1-14]

When we consider the implication of this view on parametric and computation design on the profession, it suggests the need to create models that consider environmental, economic, social, and aesthetic factors in an integrative manner to better understand the relationships between these four areas of inquiry. [1-14]

[2-4]通篇

However, early CAD software did not have the data integration, parametric capability or simulation potentials that were promised by Sketchpad.[2-4]

The work of some in-house research groups, such as Foster + Partners’ Specialist Modelling Group, and emerging communities such as Smartgeometry, inspired the creation of parametric design software, as well as numerous techniques and theories.(4) In 2003, Generative Components, a plug-in for CAD software MicroStation, became one of the first free and widely available types of parametric software designed specifically for architects.[2-4]

There is a trend in architecture towards parametric design—in which the designers focus their attention on the creation of generating algorithms rather than specific instances. In this paradigm, variants of the design are produced through varying the parameters of the underlying algorithm, and it is in the evaluation of design variants where computer simulation can play a significant role.[2-4]

For parametric studies, Rhino/Grasshopper appears to be the current industry favourite, while other examples of parametric design platforms include Dynamo/Revit, CATIA and Maya. The creation of custom computer scripts, which was a predominant mode of computational design prior to the development of Grasshopper and Dynamo, is still widely in evidence, but is now an approach that is used when the limits of visual programming are reached.[2-4]


### 复杂系统（complex system）

### 算法（algorithm）
Not understanding these algorithms, the language (codes) these instructions are written in makes the objects appear more complicated—when in reality they are simply more complicated in a digital sphere than in a physical or mechanical interaction.[1-2]

An algorithm is a set of rules or tasks that can be executed over and over again until a particular state is reached. In data sets, we use algorithms such as Bubble Sort, which sorts numeric values one after the other until all values are in ascending order. As new data sets arrive, they too can be sorted. If we think of the landscape architect as the author of an algorithm and the feedback loop consistently moving through that algorithm, then the possibilities of fast matter exponentially increases. If the landscape design process is continuous, and the algorithm is periodically updated in response to the feedback loop, then fast matter has even more potential to respond to specific site conditions, such as changing water flows, poor growth areas, or programming. With directives, the role of the landscape architect is to observe and direct, rather than create a final product. Kostas Terzidis calls algorithms a “vehicle for exploration.”21 Like the Game of Life, the designer must set the system into motion, watch it evolve, and then make adjustments or restart the game, as necessary.[1-15]

Parametric design software, such as Grasshopper, is already allowing designers to think in terms of logical questions and commands: copy this; scale according to the distance from X, etc. While Grasshopper is not iterative the way an algorithm is, it does begin to make designers respond in code, observe the results, and enact a response. Once the process is iterative, the exploration is amplified. Graphic-based coding, such as Grasshopper, also places design firmly in the realm of directives instead of documents With Grasshopper, the design work is in creating the process. The drawing, a representation of the process, can be created again and again.[1-15]


### 生成设计（generative design/modeling）
Landscape practices have recently been informed by two distinct lines of inquiry. Ecological and environmental concerns have thrust landscape and ecology into the center of design discourse in ways that explore the dynamic, operational, and even physical aspects of ecological systems as a starting point for generating design— whether landscape, building, or urbanism. Simultaneously, advances in software technologies have brought generative and associative modeling tools into the academic design studio and into the professional office, allowing for a new generation of techniques and fabrication technologies to emerge[1-4]

Such modeling techniques, which can be utilized to initiate design inquiry and ultimately generate physical form, allow for a continuous and increasing complexity of inputs to the modeling process, producing a multiplication and elaboration of possibilities that each respond to a slightly different set of priorities or agendas. Thus design is neither static nor compositional, but dynamic; assemblies of forms and components (at any range of scales and serving any number of functions) can be generated from a set of logics that can adapt themselves to circumstances, all the while maintaining their essential characteristics and operational protocols. This is conceptually not so far removed from the work of late twentieth-century ecologists, who emphasized an organism’s or ecosystem’s adaptability in assessing overall health—with the idea that various inputs could produce shifts and changes in the environment over time, and the final physical form of a healthy organism or ecosystem would change and adapt to these new circumstances.1 Multiple outcomes are possible here; physical form is malleable—it is more the functioning and operation of systems that are in play.[1-4]

This essay will examine three scales of the application of associative and generative modeling techniques in the conceptualization and making of performance-based landscape and urban form. At the scale of the human body, recent applications speak to the translation of associative modeling principles and methods into fabrication and construction processes for furnishings and elements, allowing for the generation of nonstandardized and nonrepetitive units that may better serve diverse body types and shapes and differing agendas for how to use public space. Site scale work explores the ways in which hydrology or social program or even desired experiences or relationships can inform the delineation and hybridization of landform, pathway, and gathering space. Subsequent work in both academia and practice test and push this further, with elaborations across the broader urban field, including landscape and infrastructural systems, and the generation of urban form— instigating multiplication and elaboration across large territories in ways that can adapt and adjust to specific conditions on the ground. Underlying all this is a set of dialogues between academic explorations and applications in practice that continue to reverberate and inform one another as the work advances. [1-4]

At the scale of the site, generative modeling can take on increasing levels of complexity in terms of function, program, site conditions, and any other set of technical or experienti criteria. Early studies in the academic design studio explored the various creative relationships between the protocols of remediation technologies, for instance, and the generation of responsive and productive landscape systems. The water treatment process was translated into performative criteria (basin size, flow criteria, duration, and planting and soil conditions) that could then generate a series of clustered basins. These basins could be configured differently in response to existing topographic conditions and underlying drainage patterns, producing a variety of basin configurations that all shared an inherent set of logics and performance protocols. Such early studies were translated in full design studios at Harvard’s Graduate School of Design, in which students were asked to create landform systems that would respond to water flows, inundation, and infiltration requirements—and eventually be layered to accommodate various forms of human occupation as well. In all of this, iteration, testing, prototyping, and a level of free and open-ended “play” were all at work; adaptability, and dealing with a level of environmental and human behavioral indeterminacy, came directly into play.[1-4]

From here, it’s an almost simple leap to complex urban systems—systems that include functional infrastructure, social spaces, dynamic landscapes, even building form developed according to environmental performance criteria. In some ways you could think of these advanced urbanistic and social requirements as additional sets of criteria that are plugged into the software. Here urban infrastructure can be figured to respond to advanced hydrologic agendas and adaptive water and ecological networks in the city. Buildings can be carved in response to environmental conditions and optimal sun angles for better environmental performance within the buildings themselves and better quality of public social spaces in between them. Generative systems take on multiple and diverse architectural, infrastructural, landscape, and social agendas—that allow for an almost infinite combination and recombination, testing, and evaluation—and that set up principles and tactics that can adapt responsively to conditions on the ground, administrative decisions, and evolving circumstances.[1-4]


### misc
our cities’ future is largely influenced by a third group composed of landscape architects, architects, urban planners, and engineers. These “technocrats” are shaping the physical cities and environments within which future technologies and innovations must be integrated. They must anticipate and create “space” for a future that no one can define.[1-2]

our cities’ future is largely influenced by a third group composed of landscape architects, architects, urban planners, and engineers. These “technocrats” are shaping the physical cities and environments within which future technologies and innovations must be integrated. They must anticipate and create “space” for a future that no one can define. [1-2]

At present scripters tend to be of the “lone gun” mentality and are justifiably proud of their firepower, usually developed through many late nights of obsessive concentration. There is a danger that if celebration of skills is allowed to obscure and divert from the real design objectives, then scripting degenerates to become an isolated craft rather than developing into an integrated art form.
Hugh Whitehead former head
of the Foster + Partners
Specialist Modeling Group59[1-2]

The transition will be a complex evolution from “static” built/urban environments to “dynamic” self-constructing, living, breathing, and even artificially intelligent (thinking) environments.[1-2]

What our new computational media and new methods of construction allow is a fundamental bridge between design idea and physical reality. The connection of the virtual and physical model in space can now exist in direct mirror or alternate reality of each other, as opposed to the cumbersome two-dimensional abstraction of orthographic drawings and measured scales.[1-2]

design—for instance, GIS for site analysis, Grasshopper for parametric design, and digital fabrication tools such as laser cutting and 3D milling for topographic representation.[1-12]

The recent adoption of computational and simulation techniques is not only changing the range of the technically possible, but also altering the social structures that architects operate within.[2-4]

## 参数化应用的主要方向

### 教学

One model for how this might be done is the Master of Advanced Studies in Landscape Architecture (MAS LA) program at ETH in Zurich, which is organized as a series of workshops and modules that teach programming incrementally. Beginning with a workshop introducing computational software such as Rhino and Grasshopper, the program gradually introduces more challenging concepts and coding languages including Processing and Rhinoscript. However, in addition to the hands-on training, the program also includes a three-day intensive workshop entitled “Theoretical Programming,” which introduces the theoretical fundamentals of computer programming in general and as it relates to landscape architecture, covering more advanced concepts such as genetic algorithms and agent-based systems by using interactive demonstrations and role-play.36,37,[1-12]

参数化设计相关研究内容的大类为：
### 1. grasshopper（GH）参数化设计工具界面体验；


### 2. 设计几何空间形式构建、分析、算法、生成；
#### 代理模型（agent-based model）
[1-8]通篇

Many of these problems can be productively addressed with a relatively recent approach to analyze and reveal subtle and underlying landscape structures and patterns: the computational paradigm known as agentbased modeling. This paradigm, closely tied to the computational development of artificial intelligence, has become quite popular in disciplines throughout the natural and social sciences. In general, agent-based models seek to reveal underlying and complex bottom-up patterns and structures based on the interaction of agents among themselves and with their environment. An early proponent for the use of agent-based models in the spatial design disciplines was the architect Stan Allen, who described the emergent patterns created by some of the first simple computer agents—Craig Reynolds’ “Boids”—in his influential essay “From Object to Field” (1997), although he gave no specific examples of adapting this process to an actual design problem. A small handful of architectural theorists have, from time to time, revisited the use of agents for understanding complex urban and landscape dynamics, but their application to site scale design problems remains limited.[1-8]

In this particular case, the agents do not interact with other agents but only with their environment based on a few rules defined using the scripting engine Grasshopper together with the looping plug-in Anemone.[1-8]

Quelea is a plug-in for Grasshopper, created by Alex Fischer, which enables designers to simulate user behaviour through agent modelling.(11) Through the assigning of forces and behaviours to systems of agents to create interaction, designers can create complex simulations and analyses, and generate geometric forms through the combination of simple rules.[2-5]

#### 生成/进化（generation/evolution）
[1-9]通篇

Growing access to computer-aided design and manufacturing tools has undoubtedly altered the material practices of allied disciplines. The 25-year-long catalog of work and writing on this subject within architecture, for instance, clearly demonstrates the possibility to produce complex, high-performance, and emotive form. Use of computation as a generative tool, rather than for purposes of analysis and or representation, in landscape architecture, however, has begun much more recently and, with some exceptions, has not yet demonstrated fundamental differences in approach or result from precedents in building architecture and engineering.[1-10]

Nicholas de Monchaux, an associate professor of architecture and urban design at the University of California, Berkeley, has worked since 2009 on Local Code, a project that seeks to design socially and ecologically active landscapes using abandoned urban sites in various cities throughout the United States and abroad. Many of these metropolitan areas have hundreds if not thousands of these sites, thus de Monchaux and his team have sought to find a method for systematically generating designs based on local contexts rather than designing each site one by one. To facilitate this process, de Monchaux’s team developed a set of Grasshopper components, collectively called “Finches,” which build connections between geospatial data and Rhino geometry.20 Finches includes components for importing, batch processing, and exporting shapefiles (.shp) within Rhino, meaning that different types of geodata such as parcel boundaries and topography can be combined with Grasshopper’s existing parametric modeling tools to generate 3D designs for many sites at once.[1-12]

#### CA
The use of cellular data allowed researchers at the AT&T Research Labs to map the mobility patterns of the residents of Los Angeles, New York, and San Francisco, and to compare the range and pattern of movement among these residents (Isaacman et al., 2010). [1-14]


### 3. 智能化设计——机器学习和深度学习；
Researchers such as Bettencourt and West have suggested that the growth of cities follows power laws allowing prediction of change in land cover, employment, energy flows, and a host of other factors through the evolution of a city (West, 2017). [1-14]

Researchers at the University of Cambridge have also used Twitter and Four Square data to build a model that they believe can predict gentrification, utilizing the United Kingdom’s Index of Multiple Deprivations (Rodionova, 2016). [1-14]

Parametric modeling will also impact aesthetic decisions. A team of American and Chinese researchers have utilized geotagged photographs from Flickr to identify urban areas of interest: those areas within the urban environment that attract people’s attention (Murphy, 2010).[1-14]


### 4. 结构构建信息与建构、结构分析及协同优化；


### 5. 数据管理及处理，云平台、数据库及运算；


### 6. 可持续性设计（气象数据、热、风、光、声、能源）及设计形式结构协同优化和评估；
[1-7]通篇
The consideration of atmospheric behaviours directly within design processes is made possible through the computational, which offers a major shift from the site investigation techniques of maps or diagrams favoured in landscape architecture[1-7]

Working parametrically with Rhino, Grasshopper, and small and big data, it was possible to optimize tree placement for maximum shade but with minimum tree coverage to allow uninterrupted airflow.[1-7]

Through simulation and parametric tools, it is now possible to derive the most thermally comfortable path that emerges from the aggregates of these design strategies.[1-7]

In a further example, this time engaging with Melbourne’s hot Mediterranean climate, students used Grasshopper and real-time data (wind speed data and radiant temperature) to develop a dynamic simulation, which translates temperature data into zones of thermal comfort levels – a parameter of more relevance to designers.16 Altering the different parameters within the simulation facilitates the identification of strategic points, where the designer had most potential to achieve maximum effect. The design develops through the manipulation of these specific climatic points, resulting in a new atmospheric condition in which to then consider questions of program and other aspects of experience and function (Figure 2.1.1). [1-7]

Utilizing computational modelling and simulation techniques, including CFD modelling and Grasshopper plug-ins, projects foregrounded the understanding of atmosphere as perceived space, experienced through ‘material energies’ that diversify the climatic experience to a multitude of ‘stimuli and information’27 the human body can respond to.[1-7]

Take for example the dynamics of our current weather patterns globally.[1-9]

Previously described by Kolarevic as the Digital Continuum,7 this exchange includes the possibility for geometric data generated within a digital model to be developed simultaneously through modes of analysis and optimization, representation and communication, and manufacturing and assembly. The sharing of data has allowed greater collaboration among professionals of diverse expertise and linkages across previously distinct design phases, from design conception to engineering to fabrication. The impact that this blurring of disciplinary and procedural boundaries has had on practice extends far beyond efficiencies in the design process. [1-10]

This has put areas of knowledge previously not the focus of architectural inquiry into play as generative starting points for design. More specifically, it has prompted the parameterization of intrinsic material properties and manufacturing logics in order to deploy them toward particular effect.8[1-10]

Parametric design will impact our environment at a regional, city, and site scale. Our ability to model and analyze sun, shade, wind, views, and other measures of human comfort has already created a design environment in which proposals can be simulated and adjusted in real time to create landscapes digitally shaped by these forces.[1-14]

The digital age has certainly changed those heuristics, and we are only now beginning to understand the implications of those changes. Where the architectural design process in the predigital age was one of careful contemplation, limited calculation, experienced intuition and, ultimately judgement, today’s designer can rely on an array of analytical, simulative and visualisation tools that enhance understanding of an emergent design and predict its ultimate performance.[2-1]

As hand drawing gave way to computer-aided design (CAD), and CAD to building information modelling (BIM), we now have much of the informational infrastructure and data fidelity needed to bring on the next technological era in design, characterised by algorithmic design combined with big data. Digital tools can now help designers to reason and optimise their designs with measurable results, changing the design process itself, as well as the roles and responsibilities of architects and engineers, in the systems of delivery of building.[2-1]

The methodologies and trends so skilfully described and unpacked here will lead the way for the next generation of designers to find, to paraphrase Alexander, a non-arbitrary formal order’. The mile markers of the digital turn that Computing the Environment represents are just the beginning of this journey for the building industry. Architects will always search for the ‘form which we have not yet designed’, but will increasingly do so in the context of analytical and predictive insight anticipated by the authors, a context that is, at least in part, now describable. The search for solutions will be informed and enhanced by these systems, giving designers not a new set of constraints, but rather new, greater degrees of freedom to search, iterate, evaluate, select and then synthesise answers to the challenges of our increasingly complex environment. As these methods and tools establish data-rich predictions of building performance across a spectrum of parameters that will soon evolve beyond energy conservation or daylighting, a knowledge base will emerge— the collective insight of predicted behaviour versus actual performance—that will further amplify the power of performancebased design.[2-1]

Much of the text that follows represents the best attempts to remediate the relationship of the building to the environment and the processes of design that anticipate those relationships. The resulting insights will inspire architects and engineers to create and perfect a new collection of heuristics that should lead to the next generation of high-performance design solutions.[2-1]

[2-2]通篇

While in today’s practice, numerical methods have overtaken graphical techniques in the domains of visualisation, sound and structural performance, what remains constant is the notion of simulation—the desire to get feedback from the design environment. (6) [2-2]

This is largely to do with the widespread popularity of Rhino and Grasshopper. Using an ‘open innovation’ concept, Robert McNeel enables people to create their own ‘plug-in’ design software, and this has spawned a whole ‘ecosystem’ of new and innovative computational design tools for architects. Architects are increasingly the authors of their own design environment.(14)[2-2]

Architects are largely excluded from performance evaluations of their building designs. Even with the best intentions, most decisions in this realm remain difficult to significantly impact (or measure) at the building scale as architects, engineers or urban planners.[2-3]

It is a different workflow and decisionmaking process, so it depends on the designer and how success is measured. Yehudi Kalay’s research into performance-based design finds that improvement in the design process will be brought about through feedback via performance evaluation. He argues that performance-based design should be a bi-directional design process, in which both form and the evaluative functions inform each other, and are modified throughout the design process until the designer reaches a solution when form and function come together to achieve an acceptable performance.[2-3]

The most commonly used base algorithm for whole building energy simulation is EnergyPlus, created by the United States Department of Energy as a free, open-source and cross-platform program that outputs to text files.(6) It is not a standard practice for designers to use this software due to its complexity and non-graphical interface. However, it is the underlying engine behind a range of other programs that are increasingly being used by designers, such as Sefaira, Honeybee, IES, Termite and Archsim.[2-3]

If it is carried out at early design stages, before the design is fixed, it could lead to design iterations that lower energy use. It could also make renewable energy seem like a more attractive option, and offers designers and clients more options when considering trade-offs and compromises.[2-3]

Some new tools are addressing the need for Ecotect’s functionality. Ladybug is a new environmental analysis tool that works as a plug-in for Grasshopper. Developed by Mostapha Sadeghipour Roudsari (see Chapter 19), Ladybug allows designers to import and analyse standard weather data in Grasshopper and draw diagrams such as sun path, wind rose and radiation rose. These can be customised in several ways to run radiation analyses, create shadow studies and carry out view analyses. Another tool by Roudsari is Honeybee, a plug-in that connects Grasshopper3D to validated simulation engines such as EnergyPlus, Radiance, Daysim and OpenStudio for building energy, comfort, daylighting and lighting simulation. These open-source tools are increasingly becoming more well-used and powerful (see Figures 8–11). [2-3]

In the last five years, there have been a wealth of new open-source and commercially available environmental simulation tools that are easy-to-learn and designer-friendly, such as Ladybug, Honeybee and DIVA. These tools plug in to familiar computer-aided design (CAD) software and respond to the increasing pressure on design teams to carry out early-stage environmental simulations.[2-3]

such as EnergyPlus, are collections of average weather data, including temperature and humidity readings averaged over 15 to 30 years of data based on selected weather station locations (typically airports).[2-3]

In fact, as illustrated in the later chapters of this book, there is an extremely broad range in how well, how accurately, and how often, these tools are used in practice. [2-3]

Judging from the last few years, there will be many of both and increasingly they will run natively, be accurate and quick to use, and many of them will be open-source.[2-3]

[2-4]通篇

Kjell Anderson writes that while design simulation is often seen as a specialist’s tool for predicting energy performance, the greatest value for architects is the freedom to play with design ideas and receive timely feedback’.[2-4]

1 Design tools for simulation and design: geometry, generation and analysis A selection of currently available computational tools for architectural performance analysis: red – acoustics, dark red – materials and life cycle, orange – energy, yellow – solar/daylight, green – people movement, blue – uid dynamics, purple – CAD, pink – parametric plug-ins to CAD, grey – software used but no longer supported. [2-4]

The rapid adoption of Grasshopper and its suite of simulation plug-ins demonstrates designers’ interest in computing the environment. As simulation is now accessible within the architect’s everyday design environment, it can be customised and integrated into various design tasks. Designers have gone from being tool users to tool makers [2-4]

The ways in which simulation results are displayed, interpreted and mapped onto drawings and models play a crucial role in their effectiveness in influencing the ultimate building design. Up until recently, Ecotect was the most widely used building performance simulation tool used by architects.(11)[2-4]

The examples from practice in the later chapters in this book demonstrate that architects and engineers are incorporating performance simulation, material knowledge, tectonic assembly logics and the parameters of production machinery in their design drawings. They are creating custom digital tools, enabling performance feedback at various stages of an architectural project, creating new design opportunities. Using these tools, structural, material or environmental performance can become a fundamental parameter in the creation of architectural form. [2-4]

Oxman suggests that concepts such as parametric and performance-based design can be considered ‘form without formalism’ and promote ‘new ways of thinking about form and its generation’. As designers adopt approaches that are more material-, construction- and environmentally focused, new design theory and new building forms will emerge.(12)[2-4]

benefits to the use of simulation, with the major benefits being improved performance and customised interior environments in our buildings. Anderson has identified several advantages of performance simulation by architects: first, that it enables architects to gain an intuitive understanding of how their designs can affect light, heat and airflow; second, that analyses can be done in a matter of hours, enabling more evaluations and better designs to evolve; third, that the use of simulation makes designers think about performance, and enables them to engage in higher-level discussions with engineers; fourth, that it enables designers to answer questions about a design’s performance and enables a comparison of design options in real time while designing; and fifth, that architects will often graphically map results onto a 3D model, creating clear communication devices that offer proof of design concepts.(2) [2-4]

The goal of high performance buildings must be to improve indoor environmental quality rather than simply meeting minimum standards. [2-5]

There are four primary areas of comfort that should be considered when designing a building: visual, thermal, air quality and acoustic. Visual comfort largely relates to lighting, whether this is natural daylighting or artificial lighting. Thermal comfort links with air temperature, humidity and speed. Air quality describes clean and fresh air. Acoustic comfort relates to background noise levels, as well as appropriate acoustic characteristics—primarily reverberation time, but also the types of sounds, the loudness and clarity of signals. To capture the experience of building is a nuanced condition that currently simulation tools are challenged to predict and communicate.[2-5]

However, with the rise of parametric and algorithmic design, there is a move towards mass customisation and a rejection of homogeneity. Many architects and designers are now exploring the concept of heterogeneity, of ‘differentiated’ geometry, structure and performance.[2-5]

4 How microclimate is calculated by using Honeybee and Ladybug[2-5]

First developed in 1985, Radiance is today the most widely used simulation engine for daylight and solar design. Radiance was made free and open-source in 1989 and has since been embedded in many research and commercial architectural engineering software applications. Radiance has benefited from an enthusiastic, active user group, and it continues to be developed and improved. One of the key goals in the development of Radiance was to produce physically accurate light simulation and visualisation for architecture and lighting design. Radiance uses a backwards ray-tracing algorithm, which provides a profound benefit over other calculation strategies.(9) It includes specular, diffuse and directional-diffuse reflection, and transmission in any combination to any level in any environment, including complicated curved geometries. [2-5]

Thermal comfort is a condition of mind, and a subjective evaluation, which relates directly to our bodies’ heat gain and loss, with the goal to achieve some sort of a balance between our own body and its environment. The primary factors influencing it are: metabolic rate, clothing, insulation, air temperature, mean radiant temperature, air speed and relative humidity, although psychological parameters also play a role. [2-5]

In practice today, new simulation techniques are helping designers to predict how people interact with building designs, and how to shape the designs to achieve maximum comfort and experience.[2-5]

One such open-source piece of software is OpenFOAM. It has been around since 2004, and has a large user base, an extensive range of features, and is used widely in industry and research. OpenFOAM is being used as the simulation engine for two new software projects that connect to Rhino Grasshopper: Albatross, developed by Timur Dogan, and Butterfly, developed by Mostapha Sadeghipour Roudsari.[2-5]

The goal of new simulation methods can be to transform physical phenomena, such as light, sound, air speed, temperature and humidity, into computable models. We can use the multi-faceted potentials of simulation to predict the atmosphere of our future buildings. There are intersections and interdependencies between those who design and those who develop simulations—between tool users and tool makers. Perhaps one of the reasons that this issue is emerging is because of the current intersection where designers are becoming tool makers, creating methods through which their design interests can be explored. As aesthetics can now be considered as a part of ecology, atmosphere must become a part of architectural design. [2-5]

New tools could visualise, and virtualise, the qualities of user experience in buildings, so that designers could evaluate and react to building design options.[2-5]

Finally, what is required is the integration of the representational aspects of multi-simulation in the design model—a BIM/SIM model.[2-5]

### 7. BIM（Building Information Model）建筑信息模型的参数化及平台转换数据接口；
Ultimately, CAD and documentation should further become a by-product of the design process, as the potential of a landscape BIM (LIM) method may promise, although we are some way from a synthetic implementation of such a system.[1-13]




### 8. 制造装配、机器（人）建造与3D打印；


### 9. GIS(Geographic Information System )地理信息系统的参数化融合及规划/生态分析、模拟；
Through the analysis of such data we will be able to model and test the impact of alternative urban forms to improve mobility, enhance human health, and strengthen social relationships. Current route and network analysis, utilizing geographic information systems, will be supplanted by more sophisticated analysis that will model human movement three-dimensionally in response to design changes.[1-14]




### 10. 交互硬件，实验设备数据流及分析、控制；IOT
[1-10]部分

Latent, I believe, in Kolarevic’s account is the possibility that the digital continuum can expand to also engage the input of dynamic site and material processes already underway at the start of design inquiry. Over the last 10 years, several technological developments have drastically increased landscape architects’ access to environmental sensing tools, methods of linking the values collected from these devices directly into design models, and the ability to parametrically drive digital geometries with continuous streams of data. Low-cost micro-controllers, such as Arduino and Raspberry Pi, with open-source programming environments supported by large communities of users, have enabled designers to enter the world of do-it-yourself electronics. With as little as $30 and a few hours on one of many blogs, it is possible to build a custom environmental sensing device continuously reporting information about air temperature, humidity, and pressure; visible and ultra violet light levels; wind speed, direction, and dust content; soil moisture and nutrient levels; and even complex processes such as photosynthesis. The data from these sensors can be imported into management and visualization tools, such as Excel, or streamed directly into digital modeling environments, such as Rhinoceros, using add-ons to Grasshopper. Programs such as Firefly allow a real-time connection between sensors, an Arduino microcontroller, and Grasshopper, while others such as Bumblebee allow connections to Excel such that prerecorded sets of data can be called when needed. With Wi-Fi or by logging data to external memory these devices become remote sensing stations that supply an automated and continuous feed of contextual data into the exchange that is informing our contemporary material practices. [1-10]

[1-11]通篇

As the world demands evidence-based solutions and the digital world merges with the physical, it becomes an imperative for landscape architects to harness these technologies to develop a greater understanding of their work. The availability of tools to test solutions and document impacts of design decisions enables designers to move beyond heuristics. The AGILE Landscape Project’s experimentation serves as an example of the research and development potential of DIY electronics as a means of demonstrating how sensor technology and autonomous data collection can strengthen the profession.[1-11]

Our online interactions and site-specific data generated by our mobile devices have created a new contextual and cultural layer within the landscape. Adding to this unprecedented flow of data is a growing network of sensors embedded within the environment continually gathering information.1 These systems are augmenting the built environment with new sensing capabilities that extend far beyond our five senses. The wireless network speeds and cloud computing have enabled this evolution into the physical world. Every day new sensors are being developed and deployed. Accessible analytic tools are reducing the complexities of managing this data flow. All these building blocks and insights are shaping the new landscape and opening up new possibilities for landscape architecture.[1-11]

The city’s ambitious Hudson Yards project will become one of the first quantified communities in the United States where many aspects of the built environment are measured and analyzed.7 It will become a living lab for scaling these data-rich technologies.[1-11]

In 2017, Chicago went even further and began installing a real-time network of over 500 sensor nodes.9 Each node has a combination of sensors measuring a wide array of data points ranging from pedestrian and vehicular traffic to air quality. In the hope of finding uses, the data collected will be open to the public’s use.[1-11]

This convergence of the digital and physical world offers an opportunity to enrich landscape architecture’s knowledge base by learning more about people and a design’s influence on their behavior. It also provides the tools necessary to move beyond heuristic design and ensures postoccupancy evaluation is integral to the design process.[1-11]

Collecting data for data’s sake should not be a goal. Rather, landscape architects need to be discerning about the information for improving the management and design of their projects. By selectively incorporating sensors into the design of physical space, the data collection system offers real-time information about the use of spaces. Like website analytic applications, the network can provide useful information about the number of people using the space, where they congregate, how long they occupy a space, as well as other meaningful measures of public life. The data gathered can then be combined with an array of environmental data such as temperature, humidity, sun/shade patterns, rainfall, water quality, and air quality. In addition, other available data sets such as sales tax collections, building permits, real estate transactions, and programming/event schedules can be overlaid with data to make relationships between the use of the public space and its context visible.[1-11]

The fusion of data and the physical world also opens up more possibilities for the built environment to respond to the user and the activities within it. Design elements such as lighting, shade structures, water features, and others can respond to the use of space. With the growth of mixed reality systems that visually overlay images and text, new information and experiences will become a part of the purview of landscape architecture. Landscape architects need to be in the forefront of these changes and use them to create more engaging experiences.[1-11]
[1-13]通篇

Digital toolmaking[1-13]

Digital toolmaking can be at once a methodology to describe a process applied in a professional context as well as a pedagogical method where students learn problem-solving through the creation of novel software and hardware tools.[1-13]

Thanks to many developments in this field being opensource, the sensors will often come with a source code library that greatly facilitates the programming necessary to read the values from the sensor in question. Therefore going from one sensor to a combination of sensors and their interconnection becomes a trivial programming task, often requiring only the customization of values and example code.[1-13]

Sensing tools have become a core part of the design process, both in the design education process and in the flexible generation of additional detailed site microclimatic data, such as specific characteristics of the soil, air quality, temperature, humidity, light and sound.[1-13]

FIGURE 3.4.8 Collserola National Park analysis and interpretation through intensive workshops and collaborative design discussions, demonstrating forest light daylight access, vegetation variation analyses, and an application of tablet-based (7{doubleprime}) Rhino/Grasshopper simulation[1-13]

[1-16]通篇

These experimental tests aim to simulate the potential of responsive infrastructures to modify the behaviors of riverine landscapes and their fluvial morphologies—including land accretion, vegetal proliferation, and species colonization.[1-16]

The physical model provides a tangible model that simulates sediment transport through analog interactions between synthetic sediment densities and rates of water flow. Using real-time sensing, the indeterminate becomes latent (see Figure 4.3.2) and becomes enmeshed through the introduction of technology as a new form of ecology, and eventually a nascent form of nature.[1-16]

Towards Sentience incorporates the design of a responsive infrastructural model, which attunes the projective alluvium of the geomorphology table through a series of real-time sensing and responsive manipulations as a way to curate successive sediment accretion—constantly altering and modifying the riverine landscape, privileging the evolution of ecological processes over static constructions.[1-16]

FIGURE 4.3.5 Depositor, an experimental real-time responsive model programmed to interrupt the flow of water, instantaneously redirecting it to percolate down a new fluvial direction, affecting its geomorphology Model and temporal images: Leif Estrada, https://vimeo.com/152837202[1-16]

FIGURE 4.3.6 Attuner, a real-time responsive model that monitors and modifies the alluvial morphology of sedimentation based on the fluvial flux of water, resulting in land accretion. It constantly learns from its environment and context through a feedback loop Model: Leif Estrada; photograph: Robert Tangstrom, https://vimeo.com/166623512[1-16]


### 11. 图表报告及制图；


### 12. 工具建构者(tool maker)；
[2-4]通篇

The rapid adoption of Grasshopper and its suite of simulation plug-ins demonstrates designers’ interest in computing the environment. As simulation is now accessible within the architect’s everyday design environment, it can be customised and integrated into various design tasks. Designers have gone from being tool users to tool makers.[2-4]

In the last 20 years, there has been a shift in architectural design techniques from the use of software, to the development and customisation of software. As tools have literally defined the profession of architecture(3), this shift from tool user to tool maker is profound.[2-4]

Many of the plug-ins for Rhino’s Grasshopper are building performance simulation software tools. These enable the connection of CAD geometry to simulation software natively within the architect’s design environment, offering the ability to simulate designs during the design process. This method is faster and easier for architects to integrate into their workflow. It is easier to visualise and to understand the results, and the coupling of design and analysis enables formation processes to be linked to analysis routines.[2-4]

However, the customisation of these tools requires high-level specialist knowledge. It is the creation of applications that link programs like Radiance, to Grasshopper, such as DIVA and Honeybee, which is making simulation accessible to a greater number of designers.[2-4]

The mathematical model is constructed from a mixture of wellestablished theoretical principles, some physical insights and some clever mathematical tricks. The model is transformed into a computable algorithm, and the computation of the equations over time is said to simulate the system under study.(8) In simulation, drawings are not simply expanded to models, but multiplied through time to create time-based situation-specific experiences. The epistemological nature of the architectural drawing is changing as many more layers of information are exposed and this is apparent in many aspects of architectural practice.[2-4]

There are some designers who primarily use custom parametric software that they write themselves, as this gives ultimate control, scalability and the incorporation of unique performance analyses.[2-4]

A decade ago, the majority of designers were using Ecotect. However, now it is the plug-ins for Grasshopper that offer the first tool of choice for many practices[2-4]

The integration of simulation engines with design software has the potential to address many current issues that have been identified with building-performance simulation. Recent developments in simulation software and its application in practice, as shown by the case studies in this book, demonstrate that digital design with its computational customisability through various programming interfaces enables a flexible modular computational approach. This is enabling data exchange and interoperability between simulation and design software. The accessibility of simulation engines is encouraging architects to experiment and therefore increase awareness and intuition about building performance. While there do not appear to be common approaches to optimisation, new tools such as Galapagos and Octopus are now available, which can integrate optimisation into design and simulation processes. As algorithmic design is essentially a definition of design space, the exploration of this design space is where future developments seem to lie.[2-4]


##  参数化设计方法未来发展趋势预测
### 智能化与未来
[1-6]通篇
1. Using software – as a tool, for automation: from numbers to lines to graphics/objects;
2. Writing code – as a language, for algorithms: from logic to code to forms/landscapes;
3. Engaging with the Internet of Things – as a medium, for augmentation: from static to dynamic to interactive/alive?
1. They are designed using software, algorithmic approaches, and simulation;
2. They incorporate embedded sensors, actuators, and digital/algorithmic control of electromechanical elements;
3. They provide information exchange between people and environment, in digitally mediated responsive interactions and behavior.[1-6]

The evolution of next-generation software tools for AEC design professionals will continue to take the user deeper into simulation, optimization and problem definition as mere representational concerns fall away from their preeminent position. Within this context, algorithmic modeling and visual programming software tools have risen from the shadows of academic and early adopters into a professional, cultural awareness that is starting to take the shape of a movement, if not a true shift in the architect or landscape architect’s workflows. From conferences such as SmartGeometry—which is now many years old—to a proliferation of online courses, to a recent rise in competitive alternatives in algorithmic design tools, it is now clear that algorithmic design is not a short-term fad.[1-9]

Another expectation of algorithmic design tools is they offer massive execution speedups of iterative design workflows. [1-9]

Yale professor and former VP of Autodesk Phil Bernstein says that “the next decade will see the convergence of these two distinct threads,” referring to two distinct technology realms: building techniques and digital tools.3[1-9]

To summarize, there are two primary forces at play shaping the AEC designer’s interest in algorithmic or computational design systems. The first is the convergence of realms of building techniques and digital tools, while the second is the rising value of the power of the query and the diminishing value and commoditization of explicit knowledge.[1-9]

Equipped with more robust and comprehensive training in both the theoretical and practical applications of computer programming, the next generation of landscape architects has vast potential to affect change both inside and outside the profession. [1-12]

The use of parametric and computational design processes and techniques are not only avant-garde, enhancing our ability to understand and mold our environment, but, on another dimension, are also evolutionary, shaping the way we think, communicate, and see ourselves and our world.[1-14]

Given the complexity of these factors, modeling and understanding of our dynamic environment can be greatly aided by parametric and computational design. Ecosystems are defined by flows of nutrients (including information), energy, and waste. One can envision a future in which designers can model geophysical risks such as hurricanes, tornadoes, earthquakes, storm surges, and the rise of sea level as determinants of the designed form of the city.[1-14]

A new kind of landscape design practitioner, one with degrees in landscape architecture and computer science or computational design, will emerge. All staff, however, must have a sense of the capabilities and limits of the technology. The challenge of how to make productive use of all the data at our fingertips will require the creative contribution of all of us. [1-14]


## 结论与讨论


## 参考文献（>50）
> 阅读顺序

[1]Bradley Cantrell, Adam Mekies. Codify: Parametric and Computational Design in Landscape Architecture[M]. New York: Routledge, May 2018: page range. 

[1-1]Christophe Girot. About code[M]//[1]:1-4

[1-2]Bradley Cantrell, Adam Mekies.Coding landscape[M]//[1]:5-36

[1-3]Jared Friedman,Nicholas Jacobson.Computation in practice[M]//[1]:39-49

[1-4]Chris Reed.Generative modeling and the making of landscape[M]//[1]:50-63

[1-5]Pete Evans. The parametric park[M]//[1]:71-76

[1-6]Stephen M. Ervin.Turing landscapes: computational and algorithmic design approaches
and futures in landscape architecture//[1]:89-116

[1-7]Jillian Walliss, Heike Rahmann.Computational design methodologies: an enquiry into atmosphere[M]//[1]:132-143

[1-8]Joseph Claghorn. Agent-based models to reveal underlying landscape structure[M]//[1]:144-148

[1-9]Anthony Frausto-Robledo. The role of query and convergence in next-generation tool sets[M]//[1]:171-179

[1-10]Brian Osborn. Coding behavior: the agency of material in landscape architecture[M]//[1]:180-195

[1-11]Brian Phelps. Beyond heuristic design[M]//[1]:196-204

[1-12]Andrea Hansen Phillips. The new maker culture: computation and participation in design[M]//[1]:205-224

[1-13]Luis E. Fraguada, James Melsom. Code matters: consequent digital tool making in landscape architecture[M]//[1]:225-240

[1-14]Kurt Culbertson. Technology, evolution, and an ecology of cities[M]//[1]:243-253

[1-15]Craig Reschke. From documents to directives: experimental fast matter[M]//[1]:268-278

[1-16]Leif Estrada. Towards sentience[M]//[1]:279-288

[2]Brady Peters, Terri Peters.Computing the Environment: Digital Design Tools for Simulation and Visualisation of Sustainable Architecture[M].Italy:Wiley, April, 2018: page range.

[2-1]Phil Bernstein. Foreword[M]//[2]:VI-IX

[2-2]Brady Peters,Terri Peters. Introduction—computing the environment: design workflows for the simulation of sustainable architecture [M]//[2]:1-13

[2-3]Terri Peters. New dialogues about energy: performance, carbon and climate [M]//[2]:14-27

[2-4]Brady Peters.Parametric environmental design: simulation and generative processes[M]//[2]:28-42

[2-5]Brady Peters. Designing atmospheres: simulating experience[M]//[2]:43-57
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTAzNzk2NTQxNSwxNDI5MTYzOTQ2LDEzOT
M3ODI5MDgsLTE4ODg2MzAxMjEsNjY0ODQ2NDU0LDI3ODY4OTUw
MiwtMTg5OTY0MTI4NCwtMjExOTU5MjY4LDE2NDg4NzI1MzksMT
YxNTkwNDg3OSwxMzMzMTI4NTcwLDgyMDA2Nzg1NSwtMTAwNjIw
NjA0Myw4Mzg1MDExMTgsLTk1MTYzNTAxOCwtMTU2MzY2MTI2My
wyMDI1NTQ2MDY3LC0xNDAzNDk4NDg1LC0yMjc5NDA4NDIsMjEz
NTk5NzI0XX0=
-->