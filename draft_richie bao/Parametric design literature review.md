


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

One of the roles of the group is to find better ways of doing standard analysis routines. The group develops workflows using Grasshopper with Honeybee and Ladybug, and then disseminates this knowledge to design teams. In terms of developments in environmental performance, Gallou sees that interoperability is improving, ‘designers don’t need to export and import into Ecotect as solar analysis tools are available right in Rhino’.(1) The SMG has written a custom tool for MicroStation that implements Radiance, and has created its own wrapper for widely available environmental tools Ladybug and Honeybee called Ladybee. [2-8]

By using Pachyderm in Rhino, he is able to both design and simulate using the same software, and therefore does not have to bother with translation[2-8]

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

In the last 12 years, Derix has seen that he and his team have gone through four phases of computational tool development.(2) While Java programming has been used since the early 2000s, they have created programs in a broad spectrum of languages, including C++, Java and Python.[2-16]

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

The development of computational tools tends to be tailored to a specific brief and for the automation of tasks. Derix says that computation has been used largely as a ‘problem-solving tool’ for ‘structural, geometric, climatic or statistical’ aspects of design(3); that computing has been used ‘to erase differences with engineers, not enhance (architects’) own knowledge of the key aspects of architecture: occupation and space’.(3) Both building information modelling (BIM) and parametricism serve the purposes of automating professional deliverables where computation is seen as design tool.[2-16]

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

It all boils down to this: designers want feedback. It’s that simple. —Billie Faircloth, 2016(2)[2-7]

Through the development of custom digital tools that integrate engineering calculations within parametric geometry models, the designers can more rapidly produce more relevant analysis—from days to hours or even minutes.(2) [2-8]




[2-4]通篇

However, early CAD software did not have the data integration, parametric capability or simulation potentials that were promised by Sketchpad.[2-4]

The work of some in-house research groups, such as Foster + Partners’ Specialist Modelling Group, and emerging communities such as Smartgeometry, inspired the creation of parametric design software, as well as numerous techniques and theories.(4) In 2003, Generative Components, a plug-in for CAD software MicroStation, became one of the first free and widely available types of parametric software designed specifically for architects.[2-4]

There is a trend in architecture towards parametric design—in which the designers focus their attention on the creation of generating algorithms rather than specific instances. In this paradigm, variants of the design are produced through varying the parameters of the underlying algorithm, and it is in the evaluation of design variants where computer simulation can play a significant role.[2-4]

For parametric studies, Rhino/Grasshopper appears to be the current industry favourite, while other examples of parametric design platforms include Dynamo/Revit, CATIA and Maya. The creation of custom computer scripts, which was a predominant mode of computational design prior to the development of Grasshopper and Dynamo, is still widely in evidence, but is now an approach that is used when the limits of visual programming are reached.[2-4]

[3]全书

However, one should keep an important fact in mind: parametric and algorithmic thinking is not about any one piece of computer software or any one particular syntax, but about logic, geometry, topology and interaction.[3_6-7] 

However, becoming an expert in parametric design – and scripting in particular – is a journey that can take months, if not years.[3_6-7] 

Designers must know the concepts that underlie the forms of media they use. In today’s digital media, it is primarily symbols, algorithms and programs that form the language through which we come to know what we are doing.[3_8] 

[3_9-10]
Introduction
The architectural design process is almost always iterative. Designers create solutions that, in turn, pose new questions, which are then investigated to generate more refined or even entirely new solutions. Designers often use computeraided tools to build models and help them visualize ideas. However, the vast majority of these models are still built in such a way that they are difficult to modify interactively. The problem becomes more severe when bespoke 3D models are geometrically complex. Changing one aspect of such a model usually requires extensive low-level modifications to many of its other parts. To address this problem, designers have begun using parametric design software, which allows them to specify relationships among various parameters of their design model. The advantage of such an approach is that a designer can then change only a few parameters and the remainder of the model can react and update accordingly. These derivative changes are handled by the software, but are based on associative rules set by the designer. Associative and parametric geometry, in essence, describe the logic and intent of such design proposals rather than just the form of the proposal itself. This kind of design both requires and helps to create powerful interactive tools that allow designers to explore and optimize a multitude of possibilities while reducing the amount of time it takes to do so in a rigorous manner. Engaging these parametric and algorithmic processes requires a fundamental mindset shift from a process of manipulating design representations to that of encoding design intent using systematic logic. Algorithmic thinking calls for a shift of focus from achieving a high fidelity in the representation of the appearance of a design to that of achieving a high fidelity in the representation of its internal logic. The advantage of algorithmic thinking is that it can build ‘... consistency, structure, coherence, traceability and intelligence into computerized 3D form’.1 Parametrically and algorithmically built models can react with high fidelity to their real-life counterparts when subjected not only to user changes of geometric parameters, but also to structural forces, material behaviour and thermal and lighting variations, as well as contextual conditions. Because they accurately represent the internal construction logic of the structure at hand, parametric models can also be unfolded or translated into geometries that can be digitally fabricated. This powerful digital workflow of parametric formfinding that is influenced by design intentions as well as performance analysis and digital fabrication logic is one of the defining characteristics of current digital architectural practice. Contemporary architects, such as Patrik Schumacher, partner at Zaha Hadid Architects, have gone as far as coining parametricism as the name of a new movement in architecture following modernism. He writes: ‘We must pursue the parametric design paradigm all the way, penetrating into all corners of the discipline. Systematic, adaptive variation and continuous differentiation (rather than mere variety) concern all architectural design tasks from urbanism to the level of tectonic detail. This implies total fluidity on all scales.’2 He points out that the fundamental themes in parametric design include versioning, iteration, mass-customization and continuous differentiation. It is helpful to briefly define these terms.

Versioning
Borrowed from the software development field, the term versioning refers to the process of creating versions – or variations on a theme, if you will – of a certain design solution based on varying conditions. Parametric software allows the designer to create a prototype solution that, rather than being cast in a static CAD file format, is wired – almost as a string puppet would be. This wiring allows the design solution to be tweaked and manipulated, creating new versions when new forces and conditions arise.

Iteration
Again borrowed from the software development field (see a pattern here?), the term iteration refers to cycling through or repeating a set of steps. In the case of parametric architecture, iteration can, in principle, create variation at every pass through the same set of instructions. Examples may include varying the size and shape of a floor plate as one builds a skyscraper, or changing the angle of a modular cladding system as it is tiled over an undulating surface. In addition to producing variation, iteration can be a powerful tool for both optimization and for minimizing the time needed to achieve that optimization. Using a fluid parametric system, which can give immediate feedback, a designer can generate solutions and test them rapidly by iterating through many possibilities, each created with a different set of parameters.

Mass-customization
One of the main successes of the industrial revolution is the idea of mass production. Factories and robots are able to produce thousands of copies of the same prototype. However, given the advent of digital fabrication technologies, we are now able to change the manufacturing instructions between each object. Given that the process  is parameterized and robotic, it often costs the same to mass-customize the manufactured products as it does to mass-produce the same quantity of identical products.

Continuous differentiation
Another borrowed term, this time from the fi eld of calculus, continuous differentiation alludes to a feature of versioned, iterative and mass-customized parametric work that allows for difference to occur within a continuous fi eld or rhythm. As opposed to mere variety, parametrically varied instances within an overall group, curve or fi eld maintain their continuity to other instances before and after them while uniquely responding to local conditions.

The characteristics of a parametric design system
The question then becomes, what is a parametric design system, and how can it help improve the design process or more rigorously explore possible design alternatives? In addition to the themes defi ned above, all parametric design systems share several characteristics and have similar constructs: object-orientation, classes or families, methods and, of course, parameters. Let us briefl y defi ne these concepts.

Object-orientation
Modern parametric software usually uses an object-oriented approach in its design. Object-oriented programming is a well-established computer science topic that is beyond the scope of this book, but a brief description is in order. 

The user interacts with a parametric system in a manner that refl ects its internal algorithmic structure, by creating and modifying objects such as circles, spheres, doors and walls. A parametric system usually stores these objects in an objectoriented database that can be accessed, searched and modifi ed.

Each object then has values that determine its attributes. For example, a circle will almost always contain an attribute called centre or position and another one called radius [fi g. 4]. It will also probably contain an attribute called name that identifi es the circle. It is usual for a certain value of an object to be represented with reference to the object and attribute with which it is associated. A popular notation is to use a full stop to separate an attribute from its parent object: object.attribute. Thus, if one wishes to reference the value of the radius of a circle named circleC, one might encounter the following term: circleC.radius. Similarly, the X-axis position of the same circle could be the X attribute of the position attribute of the circle, as in circleC.Position.X, and the Y-axis value could logically follow as circleC.Position.Y.

Values can either be constants (e.g. 100 m) or functions, which need to be evaluated to compute a fi nal value. The power of a function in the value placeholder of an attribute is that it can derive its value from the values of other attributes, which can belong to other objects. Consider the following hypothetical function of a radius of a circle:
C.Radius = distance(PointA, PointB)
 The above expression specifi es that the radius of a circle is not a constant number, but is derived from the distance between two points (PointA and PointB). In such a case, we call the variable C.Radius a dependent variable as it depends on other values. We also describe such constructs as associative – as in associative geometry. Association of parameters with one another allows us to derive unknown entities from known ones. In the above example, if the distance between the two points ever changes, the circle’s radius will change  accordingly. We call this feature of updating the value of one object based on changes in other values propagation. Imagine a large network of wired or associated values. A change in one or few parameters would propagate through the whole network, modifying the values of attributes and changing the characteristics of the fi nal design solution. This is the power of an associative parametric system. Objects, attributes and values are associated with one another and parameterized so that a change in the value of one parameter can have ripple effects throughout the design.

Families and inheritance
Objects that share certain characteristics can be organized as members of a class or family of objects. A class or family of doors [fi g. 5], for example, can contain many individual family members (hinged doors, sliding doors, folding doors, etc.). The advantage of grouping several objects into a family is that they can then share certain attributes with their siblings and inherit certain attributes from their parents. It is much more effi cient to organize these shared attributes only once, in a parent object, than to have to customize all the attributes and values for each offspring.

Methods
In an object-oriented system, methods are functions and algorithms that act on an object by modifying its attributes. Rather than have a large set of centralized instructions that specify how to draw circles, squares and triangles, an objectoriented system delegates, encapsulating these instructions in the class or family of each object. How an object is to be constructed or modifi ed is thus encoded as a method in the object itself. In the case of a circle, one such method could be to construct the circle by specifying the position of its centre and the value of its radius attribute. Another method could be to specify three points that circumscribe it. The system can simply tell a circle to draw itself – or it can ask a door to reverse its opening. In a modern parametric system a typical object, even one as simple as a sphere, can have many parameters and methods [fi g. 6].

Parameters
At the heart of any modern parametric system is the term parameter and so it would be wise to defi ne that term at this point. The word parameter derives from the Greek for para (besides, before or instead of) + metron (measure). If we look at the Greek origin of the word, it becomes clear that the word means a term that stands in for or determines another measure. The word parameter is often confused with variable, but it is more specifi c. In mathematics parameter is defi ned as a variable term in a function that ‘determines the specifi c form of the function but not its general nature, as a in f (x) = ax, where a determines only the slope of the line described by f (x)’.3

In parametric CAD software, the term parameter usually signifi es a variable term in equations that determine other values. A parameter, as opposed to a constant, is characterized by having a range of possible values. One of the most seductive powers of a parametric system is the ability to explore many design variations by modifying the value of a few controlling parameters [fi g. 7].

The remainder of this book presents a series of parametric design patterns of increasing complexity followed by exemplar case studies that refl ect the potential of the associated patterns. The book ends with a discussion of the future of parametric design and its potential to form a language of design. The afterword by Brian Johnson closes the discussion with advice on how to craft new solutions, based on knowledge gleaned from this book.
[3_9-10]

Parametrics is more about an attitude of mind than any particular software application. It has its roots in mechanical design, as such, for architects it is borrowed thought and technology. It is a way of thinking that some designers may find alien, but the first requirement is an attitude of mind that seeks to express and explore relationship[4_1-2]

Integrated design teams make simultaneous, interrelated design decisions across disciplines and project phases. Such decisions concern interconnected subsystems with interfaces that propagate change through the overall system and allow the design team to create many design alternatives. In addition, investment in validation of design assumptions through analysis or simulation cycles can further reduce risks.[4_1-2]

With parametric modeling, early design models become conceptually stronger than conventional CAD models and less constrained than building information models. Parameters express the concepts contained in these new models and give interactive behaviour to building components and systems. This means a change in how tools need to support design activities. For example tools like Bentley Systems' GenerativeComponents offer a fluid transition between a CAD-like modeling-based design approach on one side and a scripting-based design approach on the other side. These new parametric systems support a shift from one-off CAD-modeling to thinking in and working with geometric concepts and behaviour. Instead of building a single solution, designers explore an entire parametrically described solution space.[4_1-2]

Design is change. Parametric modeling represents change. It is an old idea, indeed one of the very first ideas in computer-aided design. In his 1963 PhD thesis, Ivan Sutherland was right in putting parametric change at the centre of the Sketchpad system. His invention of a representation that could adapt to changing context both created and foresaw one of the chief features of the computer-aided design (CAD) systems to come. The devices of the day kept Sutherland from fully expressing what he might well have seen, that parametric representations could deeply change design work itself. I believe that, today, the key to both using and making these systems lies in another, older idea. [4_7-10]

To the human enterprise of design, parametric systems bring fresh and needed new capabilities in adapting to context and contingency and exploring the possibilities inherent in an idea. [4_7-10]

It turns out that these ideas are not easy, at least for those with typical design backgrounds. Mastering them requires us to be part designer, part computer scientist and part mathematician. It is hard enough to be an expert in one of these areas, yet alone all. Yet, some of the best and brightest (and mostly young) designers are doing just that - they are developing stunning skill in evoking the new and surprising. [4_7-10]

Using patterns to think and work may help designers master the new complexity imposed on them by parametric modeling.[4_7-10]

[4_11-22]
Chapter 2
What is parametric modeling? The archetypal design medium is pencil and paper. More precisely: pencil, eraser and paper. The pencil adds and the eraser subtracts. Add a few tools, like aT-square, triangle, compass and scale, and drawings can become accurate and precise models of a design idea. Designers are used to working in this mode; add marks and take them away, with conventions for relating marks together.

Conventional design systems are straightforward emulations of this centuriesold means of work. Parametric modeling (also known as constraint modeling) introduces a fundamental change: "marks", that is, parts of a design, relate and change together in a coordinated way. No longer must designers simply add and erase. They now add, erase, relate and repair. The act of relating requires explicit thinking about the kind of relation: is this point on the line, or near to it? Repairing occurs after an erasure, when the parts that depend on an erased part are related again to the parts that remain. Relating and repairing impose fundamental changes on systems and the work that is done with them.

Many parametric systems have been built both in research laboratories and by companies. An increasing number are present in the marketplace. Certainly the most mature parametric system is the spreadsheet, which operates over a usually rectangular table of cells rather than a design. In some design disciplines, like mechanical engineering, they are now the normal medium for work. In others, such as architecture, their substantial effects started only about the year 2000.

The first computer-aided design system was parametric. Ivan Sutherland's PhD thesis on Sketchpad (1963) provided both a propagation-based mechanism and a simultaneous solver based on relaxation. It was the first report of a feature that became central to many constraint languages - the merge operator that combines two similar structures into a single structure governed by the union of all the constramts on ns arguments.

Hoffmann andJoan-Arinyo (2005) provide an overview of different kinds of parametric systems. Each is defined by its approach to constraint solving, and each has its own characteristics and implications for design work. Graph-based approaches represent objects as nodes in a graph and constraints as links. The solver attempts to condition a graph so that it divides into easily solvable subproblems, solves these problems and composes their answers into to complete solution. Logic-based approaches describe problems as axioms, over which search for a solution occurs by applying logical inference rules. Algebraic approaches translate a set of constraints into a non-linear system of equations, which is then solved by one or a variety of techniques. Constraints must be expressed before they can be solved. Large designs can embody thousands of constraints, which must be clearly expressed, checked and debugged as design proceeds. In addition to their contributions to solving constraints, several research projects have focused on devising clear languages for expressing constraints. Berning's ThingLab (1981) had both graphical and programming constructs for constraints. At the same time, Steele and Sussman (1980) reported a LISP-based language for constraints. Constraint languages such as ASCEND (Piela eta!., 1993) use a declarative object-oriented language design to build very large constraint models for engineering design. Constraint management systems, for example, Delta Blue (Sannella eta!., 1993) provides primitives and constraints that are not bundled together and with which the user can overconstrain the system, but must give some value (or utility) for the resolution of different constraints. In this system, a constraint manager does not need access to the structure of the primitives or the constraints. Rather its algorithm aims to find a particular directed acyclic graph that resolves the most highly valued constraints.

Propagation-based systems (Aish and Woodbury, 2005) derive from one aspect of Hoffmann and Joan-Arinyo's graph-based approach. They presume that the user organizes a graph so that it can be directly solved. They are the most simple type of parametric system. In fact, they are so simple that the literature hardly mentions them, focusing rather on more complex systems that address problems beyond those directly solvable with propagation. Discussed in more detail later in this chapter, propagation arranges objects in a directed graph such that known information is upstream of unknown information. The system propagates from knowns to compute the unknowns.

Of all types of parametric modeling, propagation has the relative advantages of reliability, speed and clarity. It is used in spreadsheets, dataflow programming and computei:-aided design due to the efficiency of its algorithms and simplicity of the decision-making required of the user. Propagation systems also support a simple form of end user extensibility through programming. This simplicity exacts a price. Some systems are not directly expressible, for instance, tensegrity structures. Also, the designer must explicitly decide what is known and order information from known to unknown. Propagation's simplicity makes it is a good place from which to start building an acount of parametric modeling. The rest of this chapter explains the basic structure and operation of a propagationbased parametric modeling system.

It is useful to be precise with language. The following section defines terms needed for accurate dicsussion of parametric modeling systems. These terms are generic. Any particular propagation-based system has a similar description, though some details will vary.
[4_11-22]

3.1 Conventional and parametric design tools
In conventional design tools it is "easy" to create an initial model - you just add parts, relating them to each other by such things as snaps as you go. Making changes to a model can be difficult. Even changing one dimension can require adjusting many other parts and all of this rework is manual. The more complex the model, the more work can be entailed. From a design perspective, decisions that should be changed can take too much work to change. Tools like these can limit exploration and effectively restrict design.[4_23-48]

On the other hand, erasing conventional work is easy. You select and delete. Since parts are independent, that is, they have no lasting relationship to other parts, there is no more work to do to fix the representation. You might well have to fix the design, by adding parts to take the place of the thing erased or adjusting existing parts to fit the changed design.[4_23-48]

[4_23-48]
Parametric modeling aims to address these limitations. Rather than the designer creating the design solution (by direct manipulation) as in conventional design tools, the idea is that the designer establishes the relationships by which parts connect, builds up a design using these relationships and edits the relationships by observing and selecting from the results produced. The system takes care of keeping the design consistent with the relationships and thus increases designer ability to explore ideas by reducing the tedium of rework.

Of course, there is a cost. Parametric design depends on defining relationships and the willingness (and ability) of the designer to consider the relationshipdefinition phase as an integral part of the broader design process. It initially requires the designer to take one step back from the direct activity of design and focus on the logic that binds the design together. This process of relationship creation requires a formal notation and introduces additional concepts that have not previously been considered as part of "design thinking".

The cost may have a benefit. Parametric design and its requisite modes of thought may well extend the intellectual scope of design by explicitly representing ideas that are usually treated intuitively. Being able to explain concepts explicitly is a part of at least some real understanding.

Defining relationships is a complex act of thinking. It involves strategies and skills, some new to designers and some familiar.
[4_23-48]

Data flows through a parametric model, from independent to dependent nodes. The way in which data flows deeply affects the designs possible and how a designer interacts with them. This can be illustrated with a very simple example:[4_23-48]

One of the many reasons for near-hierarchies is that the limited interactions among system parts enables a divide-and-conquer design strategy - divide the design into parts, design the parts and combine the parts into an entire design, all the while managing the interactions among the parts. The strategy works best when the interactions are simple.[4_23-48]

Using a divide-and-conquer strategy is to organize a parametric design into parts so that there are limited and understandable links from part to part. Directional of data flow assures a hierarchical model, with parts higher in the flow typically being assemblies - organizing concepts. Parts at the bottom of the flow usually correspond to physical parts of the design.[4_23-48]

Parts have names. This is designerly practice, not physical law. But there is a good reason for this -names facilitate communication.[4_23-48]

To abstract a parametric model is to make it applicable in new situations, to make it depend only on essential inputs and to remove reference to and use of overly specific terms. It is particularly important because much modeling work is similar, and time is always in short supply. If part (remember divideand- conquer?) of one model can be used in another, it displays some abstraction by the very fact of reuse. Well-crafted abstractions are a key part of efficient modeling. [4_23-48]

An important form of abstraction for parametric modeling is condensing and expanding graph nodes. In any graph, a collection of nodes can be condensed into a single node; and graphs with condensed nodes are called compound graphs[4_23-48]

A condensed node can be expanded to restore the graph to its original state. Condensing and expanding implement hierarchy and aid divide-and-conquer strategies. Parametric modelers implement this strategy to create new kinds of multi-property nodes, to support copying and reuse of parts of a graph and thus to build user-defined libraries of parametric models. See Section 3.3.7 on p. 45.[4_23-48]

Parametric systems can make such mathematics active. By coding theorems and constructions into propagation graphs and node update methods, designers can experience mathematical ideas at play.[4_23-48]

A parametric design is a graph. Its graph-dependent nodes contain either or both update methods and constraint expressions. Both are algorithms and can be changed by users, at least in principle. Long practice in using, programming and teaching parametric systems shows that, sooner or later, designers will need (or at least want) to write algorithms to make their intended designs.[4_23-48]

An algorithm is
a finite procedure,
written in a fixed symbolic vocabulary,
governed by precise instructions,
moving in discrete steps, 1,2,3, ... ,
whose execution requires no insight, cleverness,
intuition, intelligence or perspicuity,
and that, sooner or later, comes to an end.[4_23-48]

[4_23-48]
The first is "procedure":
an algorithm is a process that must be specified step-by-step. Designers largely describe objects rather than processes. The second is "precise": one misplaced character means that an algorithm likely will not work. In contrast, designerly representations are replete with imprecision -they rely on human readers to interpret marks appropriately. It is hardly surprising then that many designers encounter difficulty in integrating algorithmic thinking into their work, in spite of over 30 years of valiant attempts to teach programming in design schools. It is even less surprising that computer-aided design relegates programming to the background. Almost all current systems have a so-called scripting language. These are programming languages; developers call them scripting languages to make them appear less foreboding. In almost all of these, to use the language your must remove yourself from the actual task and your accustomed visual, interactive representation. You must work in a domain of textual instructions. This is not surprising either - algorithmic thinking differs from almost all other forms of thought. But the sheer distance between representations familiar to designers and those needed for algorithms exacerbates the gap.

In both conventional and parametric systems, the scripting language can be used to make designs. The language provides functions that can add, modify or erase objects in a model. In addition, parametric systems bring the algorithm closer to design models. They do this by localizing algorithms in nodes of a graph, either as constraint expressions or as update methods. However, designers still must grasp and use algorithmic thought if they are to get the most out of such systems

3.3 New strategies
Conceiving data flow; dividing to conquer; naming; and thinking abstractly, mathematically and algorithmically form the base for designers to build their parametric craft.
[4_23-48]

Parametric models are, by their nature, dynamic. Once made, they can be rapidly changed to answer the archetypal design question: "What if...?" Sometimes a single model replaces pages of manual sketches. On the other hand, parametric models are definite, complex structures that take time to create. Too often, they are not quick. A challenge for system developers is to enable rapid modeling, so that their systems can better serve sketching in design.[4_23-48]

In stark contract, much of the toolkit of computer programming (and parametric modeling is programming) aims at making clear code, reducing redundancy and fostering reuse. In the world of professional programming, these aims make eminent sense[4_23-48]

3.3.3 Copy and modify
Designers may throw their own models away, but will invest considerable time in finding existing models and using them in their own context. This is hardly surprising. [4_23-48]

Parametric modeling introduces a new strategy: deferral. A parametric design commits to a network of relations and defers commitment to specific locations and details.[4_23-48]

Indeed, a principal financial argument for parametric modeling is its touted ability to support rapid change late in the design process.[4_23-48]

It takes much effort to make a module work well and communities of practice develop surprisingly sophisticated module-making techniques. Almost always, the process iterates; through successive attempts modelers converge on stability.[4_23-48]

The parametric medium is complex, perhaps more so than any other media in the history of design. Using it well necessarily combines conceiving data flow; new divide-and-conquer strategies; naming; abstraction; 3D visualization and mathematics; and thinking algorithmically. These are the basics, and mastery requires more. We can expect that new technique and strategy will flow from the practices and schools that invest time and effort in the tools.[4_23-48]

Algorithms are realized as programs, which in turn are written in precise and prescribed programming languages. Almost universally, designers learn to think algorithmically by learning a programming language to accomplish design work.[4_49-64]

Hundreds of books exist, and dozens of languages have new books published every year. It aims rather to help the amateur (and often self taught) designer/programmer become better at combining parametric modeling and programming to do more effective design work.[4_49-64]

To design code is to understand the problem, decompose the problem into parts, devise data structures and algorithms for the parts and compose the parts into an entire program design.[4_49-64]

Coding translates a design into a program. It takes the abstract ideas of a design and turns them into precise instructions in some programming language. Code seldom works as written. Sometimes, coding and design go together, especially at early, exploratory stages of an idea.[4_49-64]

Programming is algorithmic thinking in action. Two programs may express an identical algorithm, yet differ in fundamental ways. Above the basics lies a craft of programming, which takes time to master.[4_49-64]

Programming enters parametric modeling in four distinct ways: parametric model construction, update method programming, module development and meta-programming.[4_49-64]

Almost all conventional CAD systems have a programming language, either internal or accessible from the system. Designers program in these languages to build and edit models. Once built, models can be changed either by hand or by the action of other programs. Certainly, parametric thinking can and does engage programming of this sort. Programmers use some of the variables that are passed to functions as parameters that link to new parametric structures created in the program.[4_49-64]

The graphical user interface (GUI) has profoundly changed our engagement with computers. It does so by providing a shared visual metaphor that enables manual interactive tasks.[4_49-64]

End-user programming comes with costs. Increasing capability adds complexity. First introduced by Dertouzos et a!. (1992) as gentle-slope systems and further developed by Myers et al. (2000), each end-user programming system has an informal function showing how difficulty increases with capability. Systems typically display steps in these functions that correspond to the need to learn new programming constructs and ideas. [4_49-64]





### 复杂系统（complex system）

### 算法（algorithm）
Not understanding these algorithms, the language (codes) these instructions are written in makes the objects appear more complicated—when in reality they are simply more complicated in a digital sphere than in a physical or mechanical interaction.[1-2]

An algorithm is a set of rules or tasks that can be executed over and over again until a particular state is reached. In data sets, we use algorithms such as Bubble Sort, which sorts numeric values one after the other until all values are in ascending order. As new data sets arrive, they too can be sorted. If we think of the landscape architect as the author of an algorithm and the feedback loop consistently moving through that algorithm, then the possibilities of fast matter exponentially increases. If the landscape design process is continuous, and the algorithm is periodically updated in response to the feedback loop, then fast matter has even more potential to respond to specific site conditions, such as changing water flows, poor growth areas, or programming. With directives, the role of the landscape architect is to observe and direct, rather than create a final product. Kostas Terzidis calls algorithms a “vehicle for exploration.”21 Like the Game of Life, the designer must set the system into motion, watch it evolve, and then make adjustments or restart the game, as necessary.[1-15]

Parametric design software, such as Grasshopper, is already allowing designers to think in terms of logical questions and commands: copy this; scale according to the distance from X, etc. While Grasshopper is not iterative the way an algorithm is, it does begin to make designers respond in code, observe the results, and enact a response. Once the process is iterative, the exploration is amplified. Graphic-based coding, such as Grasshopper, also places design firmly in the realm of directives instead of documents With Grasshopper, the design work is in creating the process. The drawing, a representation of the process, can be created again and again.[1-15]

[3_22]
PART I ALGORITHMIC THINKING

From the time of ancient Vitruvian geometric ideals to modern Corbusian regulating lines and Miesian modular grids, architecture has always been bound to (if not by) a conscious use of numbers.’ Brett Steele (‘Weapons of the Gods’ in The New Mathematics of Architecture by Jane Burry and Mark Burry)

Rather than rely on an intuitive search for a solution, parametric design often involves precise, step-bystep techniques that yield a result according to rules and inputs. This way of thinking about the process of design as a rigorous rule-based system is referred to as algorithmic thinking. As Steele’s quote above hints, mathematical knowledge and algorithmic thinking have always been the traits of an architect, certainly at least since the times of the ancient Egyptians and Greeks. Today, individuals who wish to use parametric design in architecture find themselves faced with the challenge of learning algorithmic concepts (as well as mathematics) that are more familiar to software programmers than to designers. Behind every piece of software is a set of precise instructions and techniques that interact with the user, respond to events, and read, manipulate and display data. Collectively, we call these instructions and techniques algorithms. Derived from the name of a Persian mathematician (Muhammad ibn Musa Al-Kwarizmi), an algorithm is defined as a set of precise instructions to calculate a function. An algorithm usually takes input (which can be empty or undefined), goes through a number of successive states, and ends with a final state and a set of outputs.

Learning programming concepts does not necessarily ensure that a designer will learn algorithmic thinking. The challenge is not dissimilar to learning cooking: one can learn the basics of mixing ingredients, heating, baking and so on, yet there is no guarantee of becoming an accomplished chef. As with most things, it takes a love for the craft, a methodical mind, some talent and, most importantly, practice. The metaphor also applies to the process itself: in the same way that cooking recipes vary in complexity, elegance and the taste of the final result, algorithms also vary in complexity, elegance, and the aesthetic and performative characteristics of the resulting design solution. While some recipes are invented from scratch, most are modifications of and variations on older recipes. The same applies in parametric design. The Internet is teeming with opensource algorithms that are offered for others to learn from, modify and expand. Beware, however, of the microwave variety: algorithms and definitions that are pre-packaged such that you cannot investigate and modify them. These types of algorithms are not always clear and readable, and this is where a book such as this becomes useful. The elegance, modularity and readability of an algorithm usually have a direct relationship to its ability not only to produce elegant design solutions, but also to be understood and modified by others.

The good news, however, is that most designers wishing to use parametric techniques usually need to solve a relatively small and well-bounded design problem (unlike software developers, who create large and complex software products). For example, they might need to create a parametric building façade or a roof structure. They might need to mimic a natural phenomenon to create a design concept for their project. Algorithmic thinking allows designers to rationalize, control, iterate, analyze, and search for alternatives within a defined solution space. In the next section, we will explore the basics of algorithms. This brief introduction cannot replace a full discussion of algorithms and the inner workings of computer programming languages. For that information, there is a plethora of books on programming, online resources and university courses that are dedicated to this topic.
[3_22]


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

Foster + Partners founded the Specialist Modelling Group (SMG), The SMG is an inhouse consultancy, comprised of about 24 digital design specialists with expertise in geometry and modelling, parametric design, computer programming, building information modelling (BIM), digital fabrication, structural engineering, thermal comfort, lighting, acoustics and wind analysis, and post-occupancy evaluation and real-time sensoring.[2-8]

The SMG believes that there is a need to integrate architecture and engineering on a digital workflow level.[2-8]

Open-source software enables the team to access the source code, so that they can customise the tool to meet their needs. An in-depth understanding of how the software is working is crucial, so that it can be customised to carry out specific analysis tasks.[2-8]

Commercially available software, open-source code and bespoke software solutions are often combined together in creative new design workflows that enable design teams to realise the office’s innovative and sustainable architecture.[2-8]

De Kestelier concludes that ‘the next step is to design buildings based on the user experience, to design buildings that feel great, that are amazing, and that just work. Because the tools are better, we can do what architects did before by intuition and experience, to determine what it is that you want to feel, design the surfaces around that, and give the user the experience they expect’.(1)[2-8]

Their research approach is driven by the desire to improve the ‘collective intelligence’ of the building industry. They pursue this not only through their many planning and architecture projects, but also by redesigning systems of design using computational approaches.[2-9]

As opposed to the current trend with visual programming where fewer people are required to learn to program, designers at SuperSpace are finding they have to become even more technical and to increase their development skillset.[2-16]

SuperSpace develops its own software in line with its agenda to build an experience-based, human-centric, spatial architecture. This approach allows for an even deeper dive into human comfort and wellbeing. Through a holistic analysis of environments, interior programmes and material assembly, SuperSpace simulates and optimises building performance to achieve dynamic experiential goals.[2-16]

For urban design, the team of designers creates flexible tools, divided into components, with compatible inputs and outputs, where applications can be replaced by their manual input and output, thus many different workflows can be assembled.[2-16]




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

In terms of future applications for this kind of simulation, she explains: ‘human behaviour is complex, the ways people determine how to behave in a new environment depends on many factors. Yes you can model a simple behaviour model like a random walk, but you’d be more close to reality if you base your simulation on real data collected from the users’.[2-7]

SuperSpace is a multidisciplinary team that champions the use of bottom-up algorithms and has pioneered many models of artificial intelligence (AI), artificial life (AL), spatial analysis, data visualisation, and spatialisation in architectural and urban design.[2-16]

Derix argues that while explicit parametric models will eventually automate the definition of metrically efficient spaces, it is a bottom-up approach that will enable architects and urban designers to focus on designing the experience of users and qualitative spatial correlations.(4) [2-16]

He felt that the functionalist tradition was an oversimplification, and that through the complex emergent systems, sought to determine the structure of the pre-industrial architecture and cities. In the systems developed, the designer ‘became a “systems designer” and the ultimate design was the emergent outcome of the complex interactions taking place under the software’s control on the aggregating system’. Coates explains: ‘If architects are systems designers they will need to think algorithmically’.(5)[2-16]

Derix argues that three strands provide the basis for a humancentred design methodology: first, space as heuristic generation— generative algorithms and mathematical representations; second, interactions in the field—distributed computing through agent modelling; and third, cognitive conditions—spatial cognition theories and phenomenology.[2-16]

#### 生成/进化（generation/evolution）
[1-9]通篇

Growing access to computer-aided design and manufacturing tools has undoubtedly altered the material practices of allied disciplines. The 25-year-long catalog of work and writing on this subject within architecture, for instance, clearly demonstrates the possibility to produce complex, high-performance, and emotive form. Use of computation as a generative tool, rather than for purposes of analysis and or representation, in landscape architecture, however, has begun much more recently and, with some exceptions, has not yet demonstrated fundamental differences in approach or result from precedents in building architecture and engineering.[1-10]

Nicholas de Monchaux, an associate professor of architecture and urban design at the University of California, Berkeley, has worked since 2009 on Local Code, a project that seeks to design socially and ecologically active landscapes using abandoned urban sites in various cities throughout the United States and abroad. Many of these metropolitan areas have hundreds if not thousands of these sites, thus de Monchaux and his team have sought to find a method for systematically generating designs based on local contexts rather than designing each site one by one. To facilitate this process, de Monchaux’s team developed a set of Grasshopper components, collectively called “Finches,” which build connections between geospatial data and Rhino geometry.20 Finches includes components for importing, batch processing, and exporting shapefiles (.shp) within Rhino, meaning that different types of geodata such as parcel boundaries and topography can be combined with Grasshopper’s existing parametric modeling tools to generate 3D designs for many sites at once.[1-12]

At Smartgeometry 2016, Phil Bernstein introduced the generative design concepts and explained that this process allowed the automatic creation, evaluation and evolution of thousands of options to meet the project goals.(15) The aim was to make informed data-driven trade-offs. Generative design paired with performance evaluation was used to develop the brief, the interior concept and layout, the design components and furniture, and to determine how the project could be evaluated. Further feedback came from the construction of full-scale mock-ups. Autodesk moved into its new space in late 2016.[2-7]

SuperSpace employs data-integrated techniques—generative models associate data to express morphologies and analytical models are used to learn patterns in data. The group applies computational design methods to predict human behaviour and map social and physical trends within organisations and cities: they ‘unlock the creative potential within big data’.(1) [2-16]

Derix explains that once the environmental conditions are computed and understood, then you need to operate on these patterns, and this requires a generative approach.[2-16]

#### CA
The use of cellular data allowed researchers at the AT&T Research Labs to map the mobility patterns of the residents of Los Angeles, New York, and San Francisco, and to compare the range and pattern of movement among these residents (Isaacman et al., 2010). [1-14]

#### 参数化/算法模式 parametric patterns
-controller, force field, repetition, tiling, recursion,subdivision, packing, weaving and branching[3_26]






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

At a larger scale, studies of buildings and cities in use and their related environmental impacts and emissions are being informed by real-time data and simulated to show impacts over time. One such initiative, the Megacities Carbon Project, demonstrates new measurement and simulation techniques for urban emissions using computational design tools. Figure 1 shows the Los Angeles pilot study, which simulated and analysed data about emissions and their sources at urban and regional scales.(4)[2-6]

CARBON CALCULATOR Another comparative tool using a firm’s own projects is the Carbon Calculator developed by engineering group Thornton Tomasetti’s in-house research team CORE studio (see Chapter 15). CORE developed a tool that was able to calculate the total embodied energy and carbon of any design configuration early in the design phase. (11) The team referenced the Inventory of Carbon and Energy (ICE) database to create an array of Grasshopper components that calculate and visualise embodied carbon in real time with the design process. The tool shows data for the total amount of embodied carbon emissions produced by the structural engineering projects carried out by the firm. While currently only using their own data, this application could be a model for sharing and comparing other data sets. They also developed the FootPrint app that shows the carbon footprint of all of their offices by year, emissions source and office location for easy comparison.(12)[2-6]

CREATING USEFUL INFORMATION FROM REAL-TIME ENVIRONMENTAL DATA Predicting environmental performance is important, as is collecting post-occupancy data, but what about in-occupancy data? How can designers collect and make sense of data about their buildings while they are being used, in order to make them run better, fine-tune systems and prepare for future renovations? Pointelist is another collaboration by KT Innovations, in this case a way of collecting and making use of environmental data using sensors.(15) After years of experimenting with low-cost sensor networks on their own projects, they have developed and commercialised a product for designers: a low-cost sensor network of data points that test temperature and humidity that uses existing sensor technologies in ways applicable to designers. The data collected by the sensors is automatically uploaded using Wi-Fi to the online interface every five minutes, and data can be visualised, compared and graphed easily using a desktop or mobile device. Pointelist is new, and so far in beta testing only, but it could have a big impact on how designers are able to gather knowledge about buildings in use. [2-6]

10 Autodesk Research, Project Dasher, 210 King Street, Toronto, Canada, 2011 These diagrams show locations of sensors deployed in the office cubicle and the prototype physical layer. The sensors collect data on temperature, humidity, light, motion, CO2 and send it via Wi-Fi.[2-6]

The appropriate and interactive real-time data visualisation is highly successful in this project and allows the building’s data, too often not shared with or understood by occupants or the design team, to be collected as a source of useful information potentially informing future similar projects. [2-6]

As programmable hardware becomes cheaper and easier to use, there are new possibilities for embedding climate responsive behaviour into architectural elements. Architect and software developer Timur Dogan (see Chapter 19) and Peter Stec worked with architecture students to develop a workflow for rotating mirrored light shelves that can tilt in two directions based on the sun’s direction, using real-time monitoring and rapid prototyping.(16) They used Radiance for daylight simulations and Arduino circuit boards to actuate and control the system. Dogan and Stec credit ‘the convergence of rapid prototyping, parametric design and environmental modelling software’ as making it easier to ‘evolve a dynamic, direct-reflective daylight redirection system’ that can be compared against normal static louvre systems.(16)[2-6]

USE DATA: COMPUTING LIFE-CYCLE AND REAL-TIME VISUALISATION Designers are using computational design and simulation at multiple scales to experiment in order to better understand the human dimensions of comfort and experience as well as energy use. Collecting, sorting and storing data about a building is challenging, and there needs to be more focus on monitoring and evaluating buildings over time. Sustainable design is not a ‘solution’ or an end state; its meaning is constantly shifting and not the result of any one intervention. The location of the building and its uses, the selection of materials and specifying of construction processes, the designing of interior relationships and sizing of rooms are all among the myriad of decisions that are made during the sustainable design of buildings. The next chapter will continue to examine ways in which designers are seeking to collect, analyse and usefully integrate real-time site and climatic data to improve their designs.[2-6]

The Private Microclimates workshop cluster at Smartgeometry 2014 was led by architects Mani Williams and Mehrnoush Latifi, and aerospace engineer Daniel Prohasky, all from RMIT. They investigated how to gain and visualise environmental feedback for wind and airflows by using hybrid physical and digital methods.[2-7]

In 2016, SIAL researchers carried out another real-time investigation of gaining feedback from digital and physical environmental data sources[2-7]

A fabric designer provided expertise in cutting the fabrics and selecting fabrics with various thermal properties, such as moisture wicking, and varying levels of absorbency, which impact the thermal behaviour of the structure. They used digital tools to visualise the data that they had collected from the sensored physical prototypes. In this workshop, participants developed a unique process for design that enabled them to design the modules at 1:1 scale, to make physical mock-ups and then to add changes to their prototypes in an iterative process based on the feedback that they had gained from the visualisation. The installation functioned as an experiential prototyping platform at full scale with many potential applications for the building industry, given that every building contains environmental microclimates.[2-7]

14 Philippe Rahm, simulation showing microclimates and people, Jade Eco Park, Taichung, Taiwan, 2012–2016[2-7]

Transsolar KlimaEngineering provided expertise relating to the CFD analysis as the flow of air and microclimate was essential to the design. Rahm explained: ‘we began not to create the program, but first to create the climate’.(18) The site is very hot and ‘200 days per year it is more than 29 degrees celsius on this site’. So the design uses passive cooling strategies, and trees are planted for shading, and the different areas of the design are programmed around the air velocity, air temperature, noise levels and pollution levels. Rahm began by reinforcing cooler areas, diagramming heat maps, and considering seasonal and daily events on the site, and then thinking of the function[2-7]

The trajectories and experiments highlighted in this chapter point to exciting new directions for ‘computing the environment’. There is a need for a broader consideration of the ‘environment’, including not only built space and nature but also atmosphere and human behaviour. The Smartgeometry workshops, perhaps due to their changing themes within digital design, and their ability to curate and peer-review participants and topics, offer important venues for digital design experimentation. The works in this chapter point to more ambitious roles for architects in the simulation process. The increasing ease and speed of gaining feedback from physical and virtual testing enables new ways of designing. Real-time feedback, design for interaction with the environment, not only measuring or simulating its behaviour, and the inclusion of new metrics like sound, are flourishing in experimental projects, and are likely to come to mainstream practice in the near future.[2-7]

At the same time, they took a collection of recordings of the signature elements of San Francisco, birds singing, types of traffic, fountains, street musicians, the elements that make the city unique, and through comparing the different sounds of the city, the design team could better define the soundscape that they aspired to create.[2-8]

simulation gives young architects a tool to understand how the environment will work inside the building. These simulation tools let them understand how the light comes in’.[2-8]

deployment of high-density, low-cost sensor networks that offer real-time feedback of environmental conditions on a site. Paired with other environmental standards and data sets, it offers designers the possibility of knowing the particular thermal conditions on their sites. After tests with commercially available, off-the-shelf sensors, beginning in 2007 at Loblolly House, the firm developed its own wireless sensor networks. The designers tested these systems in two major installations in 2013, including the renovation of building 661 at the Consortium for Building Energy Innovation at the Philadelphia Navy Yard.(6) They used their own offices in a former bottling facility in the Northern Liberties district in Philadelphia as a test bed in 2014, installing 300 temperature and humidity sensors in the facades, roof, interiors and floors before they moved in. They aimed to harvest fine-grained environmental data to identify locally specific design solutions for increasing comfort and reducing mechanical systems.[2-9]

By bringing together multiple sources––their experienced observations on the site, the outputs of the real-time sensor data and the government-issued weather data from the site––they were able to learn about how the building’s performance varied around the building and over time. This information informed their renovation of the space, and various studies including interior daylight and airflow analysis. Based on the feedback, they decided not to use mechanical cooling, and rely on using desk fans and operable windows, and to monitor the environment using the sensors. In addition, the team gathered weekly survey data from staff about comfort levels and satisfaction with their work environments, sending emails to staff about options for keeping comfortable in the office in relation to outdoor conditions.(6) This qualitative data produced another layer of data about the environment, and it was useful for making decisions about the building and understanding its performance. The environmental performance of the office is continually being tracked and monitored, and this means that it is being updated and adjusted, creating an ongoing model for analysing the environment.[2-9]

At Tulane University in 2013, they installed a network of 150 sensors in the existing School of Architecture building, to understand mean radiant temperature across the facades. Using this data, they designed a renovation and addition with the goal of achieving maximum comfort using minimal energy. The team was surprised to find that in the winter, there was significant temperature stratification and the mean radiant temperature results were inconsistent throughout the building, whereas in the summer the interiors were relatively comfortable and consistent.(7) This data was plotted in a psychrometric chart, compared with other data, and considered in relation to the existing forced air system, which appeared to adequately achieve required comfort levels in the summer. The sensor data enabled them to predict areas of higher interior comfort and to inform systems sizing and design. Test cases such as this have proven to the team that sensor networks can offer useful data in the design process, and the team is planning further installations in other projects to be able to predict performance and tune the architecture to the local environment.[2-9]

In summer 2016, the wireless sensor network research was branded as Pointelist, and it offered free kits to beta testers.(8) The hardware and software can be integrated with a web app, and users can export .csv files to use the data elsewhere. It has an open .api file extension, making it suitable for users to adapt to their own needs and workflows. Pointelist enables the collection of realtime temperature and humidity data, sending environmental data over Wi-Fi in five-minute intervals.[2-9]

KieranTimberlake is able to create its own custom weather files, and combine the real-time sensor network data with weather station data. Over the past year, the office has installed 10 low-cost custom weather stations, known as personal weather stations (PWS), on sites for clients, and it has found that there is a growing market in this area.(10) The designers find that the data does vary from site to site, even within a neighbourhood. [2-9]

The sensor and weather data can have an impact on the building’s form to work in synergy with local environmental conditions.[2-9]

The Solar Modeler tool was designed to use typical meteorological year (TMY) data or site-based sensor measurements and to give analysis in a format that would be useful as feedback for the design process. It is designed to integrate with Rhino and it has evolved on the basis of user feedback.[2-9]

GXN used Ladybug for Rhino, which utilised climate data. This allowed designers to understand and design for specific local site conditions. Ladybug provides visualisation tools for wind, rain, sun-path, solar isolation and cloud cover. Jensen has stated that ‘90 per cent of a building’s form is decided in the first 10 per cent of our design process. To inform our architecture we use software that provides live feedback on daylight quality and environmental impact, right from the first early sketches’.(2) [2-10]

Using sensors, energy modelling and an indoor environmental quality app, guests can track the impacts of their stay, monitoring water and energy consumption, daylight levels, air quality, temperature and humidity levels. The app, which is still under development, was designed to monitor real-time energy sources, so that guests could see which proportion of the energy they use is from renewable sources. [2-10]

GXN has a broad focus, seeking to support design processes and advance multiple streams of green research. The daylight simulation and early-stage design optioning are central to the architects’ work, but in the future they aim to focus more on real-time energy monitoring, building on the success of their Green Solution House. It is imagined that this stream of inquiry will lead to new workflows for architects and more interactivity with people in their design environments. GXN’s work illustrates not only how a variety of environmental computation approaches can shape building form, but also how this can shape users’ behaviour.[2-10]

2 Foster + Partners, Samba Bank New Head Office, Riyadh, Saudi Arabia, under construction Parametric facade design tool by BuroHappold for glazing optimisation to maximise daylight factor, and to limit solar and conduction gains [2-11]

4 BuroHappold, current process map As the number of analysis programs increases, how these programs share data and interact in design workflows grows organically.[2-11]

5 BuroHappold, proposed process map BuroHappold has created a variety of design workflows, depending on the stage and complexity of the project, and accuracy and efficiency of the results needed.[2-11]

OPTIMISING DESIGN SOLUTIONS
Typically, when confronted with a complex performance issue on a project, BuroHappold will implement a parametric design approach, to generate and analyse a range of building designs. The geometry and performance of these options can be visualised, which gives the architects and engineers knowledge of what works and what does not, and the relationship between form and performance. However, as the computer is generating and analysing the geometry, this computational process can be iteratively looped, so that the design ‘evolves’ to find a better performing building system. This optimisation strategy is called a ‘genetic algorithm’ as it imitates the process of evolution to optimise buildings and/or parts of buildings. The technique can involve hundreds of loops and result in the generation of thousands of different options. However, this technique can yield new and better performing geometries than could be found otherwise. This technique is powerful, but as Knott explains, the most important questions are still, ‘what is the goal of the optimisation?’ and ‘what is being optimised?’.(3)[2-11]

Performance issues involve multiple parameters, and the selection of parameters, and how the parameters are weighted, are key questions being investigated, which are always project specific. While optimisation is often talked about, Knott says that often it is best not to optimise at all—better results can be found more efficiently just by using parametric modelling, analysing all different options, and then visualising the trade-off curves.(3) Knott explains that ‘there are benefits to keeping the computational processes relatively simple as it is a balance of speed and graphic sophistication’. He has developed a library of digital tools in Excel, many of which now have user interfaces that enable other designers and engineers to use them. Additionally, he has developed an in-house database so that the methods and results from previous projects can be easily referenced.(3)[2-11]

The SMART Solutions group develops computational tools to model, analyse and map performance.(4) Many of these design tools have been implemented in Rhino and Grasshopper, such as SmartForm, SmartMove and SmartSpaceAnalyzer.[2-11]

Currently, Knott, together with the SMART Solutions group, is developing a Rhino Grasshopper digital tool that outputs both categories of metrics. Looking to the future, Knott argues that these soft metrics will become increasingly important and that the focus will shift away from energy and carbon. To design for sustainability is to design all aspects of the experienced environment, considering air, humidity, and temperature and people’s wellbeing.[2-11]

[2-12]通篇

Designing the performance of the invisible aspects of the environment, such as light, air and sound, is at the heart of Max Fordham’s work, and the firm’s approach to computing the environment incorporates digital simulation, physical testing and multiple overlapping analyses, using digital tools to visualise and realise experiential aspects of architecture.[2-13]

Cramp explains: ‘We used a program created in Grasshopper for Rhino to run a genetic algorithm to size the pyramidal roof lights to keep out direct sun year round, and a second program to check for the transfer of specular reflections between panes of glass into the gallery below’.(2) Parametric modelling was an important part of the design process, and the team developed and programmed algorithms to simulate diffuse daylight and direct sunlight into the gallery spaces. Max Fordham partner Hareth Pochee adds: ‘Rather than directly designing objects, we design algorithms (sets of rules) that in turn design the objects. Thousands of design options were tested by rapid, virtual prototyping to find one or more solutions that were the best fit’.(2)[2-13]

Increasing environmental performance specifications means that multiple scales and modes of analyses are required. There is a rapidly growing number of digital tools for environmental analysis, and on a given project, Max Fordham employs a variety of tools. Cramp says that the team regularly uses Ecotect, DIVA, Ladybug and Grasshopper, as well as writing custom scripts and plug-ins for software like Radiance as needed. Depending on the project, the designers also use open-source codes such as OpenFOAM for complex fluid dynamics (CFD).[2-13]

The office developed geometric models to predict the acoustic environment inside each space, with particular attention to the surface finishes and location.[2-13]

White has several specialist teams of designers and researchers, focused on developing and utilising digital design tools for environmental simulation and computation. For example, the Dsearch group, which is led by Jonas Runberger, focuses on digital design tools and parametric design. A collective of about 12 designers has formed a working group focused on building performance simulations (BPS), specifically relating to daylight and energy modelling to explore the ways in which building performance simulation tools are used in the office.(1[2-14]

The designers are spread between different offices, and specialise in using digital tools for daylight studies, energy modelling, thermal comfort calculations, wind simulations and life-cycle-based analysis.(2)[2-14]

[2-15]通篇

This chapter explores some recent projects where the ZHACODE group has created innovative site-specific responses, involving a range of environmental parameters.group works to integrate concepts for daylight, solar shading, wind studies and visibility analyses into projects of many scales. Some projects that have provided great breakthroughs in workflows and tools development remain unrealised, and the design teams learn from these and apply lessons in future projects. Ambitious and unbuilt projects are explored here as showing trajectories of environmentally ambitious parametric design.[2-17] 

The team first works to abstract a complex design into geometric rule sets. Then it develops custom digital tools or adapts existing ones that integrate computational fluid dynamics (CFD) into the parametric geometry model. [2-17] 


### 7. BIM（Building Information Model）建筑信息模型的参数化及平台转换数据接口；
Ultimately, CAD and documentation should further become a by-product of the design process, as the potential of a landscape BIM (LIM) method may promise, although we are some way from a synthetic implementation of such a system.[1-13]

2 KieranTimberlake, iterative life-cycle analysis (LCA) workflows using Tally, 2013 Tally enables early-stage design feedback directly through Autodesk Revit, allowing designers to compare design options and benchmark environmental impacts, based on material selections as part of an iterative design process.[2-9]




### 8. 制造装配、机器（人）建造与3D打印；
#### 数字建造 digital fabrication/formation
In other, more recidivist cases, designers impose form on matter through more familiar parametric, fabrication, and most overtly, geometric processes. In some examples, formation is over-determined by the technics of fabrication.[5_8]

[5_10-15]
THE MATERIALLY RESPONSIVE PARAMETER

In recent years, designers have developed processes for layering performance-based feedback into the early stages of design development.4 This is often a response to the tendencies of a construction industry that values efficiency-resulting in excessive waste-over environmental steadfastness. However, a systematic design process, applied specifically to material constraints could frame awareness of the interconnectivity between the mediums of ecology, parametric modeling, and CNC fabrication. David Gissen outlines an architectural ideology based upon the definition of Architectural Political Ecology.5 Gissen defines a variety of concepts to accomplish a “production of nature.” He is attempting to look beyond the superficialities of so-called “green” design to a set of strategies that embrace substantive design rather than the relatively mundane aesthetics of environmental awareness as an applied layer to architectural design. This type of substantive design is defined by the tangible knowledge of material characteristics, such as: dimensional properties, durability, deformation, waterproofing and weathering (if applicable), connection types, relative costs, color, texture, and finish. These characteristics define some of the performance criteria, which can and should be layered into the early stages of each design process, linked to their formal expression through parametric design. Further, these performance-based characteristics can be identified as the primary device for delimiting form through parametric design, most often through geometric relationships. 

“Form-finding” as defined by Andrew Kudless is “the self organization of material under force to discover stable forms.” Using both analog methods of tension-only models hung in chain and fabric, and using advanced software tools such as Thrust Network Analysis (Philippe Block), there are many examples included in the following pages of work which attempt to respond to the form as it falls into stasis with gravity. These tests can result in forms hung in space as with Feathered Edge (p. 198), by Ball Nogues, or the fabric-formed beams of Mark West and C.A.S.T. (p. 128). These forms can also be inverted to create compression-only forms as with Philippe Block’s Catalan Thin-Tile Vaulting (p. 154).
[5_10-15]

The intent of this text is to map through materiality the simplest methods for making complex parametric forms, whether constructed by unskilled labor, or using complex systems of hybrid materials and assembly with 7-axis robots.[5_10-15]

This text will provide clear narrative and diagrammatic, dissections of the computational and physical construction processes used in some of the more inventive solutions constructed since the advent of widespread parametric design.[5_10-15]

The ubiquity and availability of CNC technology was driven by the mass production of servo and stepper motors, the most widespread method by which computers precisely control machine components.[5_10-15]

More recently, the use of 7-axis industrial robots has enabled a much broader array of processes and materials to be computationally manufactured. The end-effectors, attached and controlled by these arms, are as diverse as the materials they can process. These have included all of the typical cutting systems (circular saw, router bits, water-jet, plasma and laser-cutting), as well as grippers, benders, hot-wire cutters, and others. Additionally, the robots’ flexibility has allowed them to break the bounds of the factory floor, and operate on site.[5_10-15] 

While material knowledge gained through computational tools is different, it can be argued that this understanding is not less informed but fundamentally different, more directly linked to the interaction between tool and material [5_10-15] 

THE APPLICATIONS (SOFTWARE) OF PARAMETRICS
Parametric software creates systems defined not by Cartesian coordinate systems, but by linkages and constraints between geometry. By their nature parametric systems do not have a specific solution but are capable of accommodating a range of possibilities.6 The mapping of material constraints can be parameterized in two ways, through scripted or defined variables or through the definition of geometric relationships. As of publication, there are four primary pieces of software, which are typically employed for this type of user-defined parametric mapping: Gehry Technologies Digital Project, Robert McNeel and Associates’ Grasshopper 7 scripting plug-in developed for Rhinoceros, and Dynamo, objected-oriented scripting for Autodesk Revit and Generative Components developed by Bentley Systems, Inc.[5_10-15]

The underlying geometric definitions of Digital Project allow designers to map limitations across a surface or across its edges. These limitations fail when an iteration of the surface is too dramatic for the constraints of the respective construction system. The topological nature of a form, when combined with the complexities of parametric systems, allow for variation through relationships, instead of individual parts. Additionally, other components of the software (Knowledgeware) can be used to map the maximum deviation of each piece of the system away from the original surface. When the deviation becomes too great compared to predefined standards (for aesthetic pairing or legibility of form) the system will identify the portions beyond those limits, so they may be adjusted. [5_10-15]  

We are left to determine a set of values, in a process defined through experience, to guide our sense of craft with the machine[5_10-15]  

[5_16-242]  案例某部分参考

#### 3d printing
3D Printing Architecture impressively brings together myriad important technologies that will play key roles in the application of 3D Printing to architecture. What sets it apart, and ahead of, the current literature is how it impressively integrates computational generative design of complex structures, simulation of functional performance, and multiple manufacturing process centered on 3D Printing into new digital workflow constructs. This results in a digital thread throughout the entire design and production supply chain including materials, manufacturing logistics, assembly logic, cost, and validation and verification. 3D Printing is the integrative production technology that ties these together, enables new advances in the individual technologies, and sets the stage for a digital design and production paradigm where increased design freedom is availed, informed design decisions can be made earlier in the process, and appealing system effects are exploited throughout the value chain [6_Foreword]  

These have taken 3D-printed architecture to new heights. While the examples highlight the power of the 3D Printing technologies when integrated in digital workflows focused on architecture, the implications and knowledge are much more broadly impactful to other types of products ranging from aerospace structures to medical devices.[6_Foreword]

Any structural connection has to both enable the continuity of the geometric form and provide the required mechanical and functional performance and durability. A major challenge, in addition to the assembly and fabrication ones, is the complexity of analyzing and qualifying the mechanical performance of the connection, either through existing design codes or more sophisticated but expensive numerical analysis and experiments. The 3D-printed node approach elegantly solves this by decoupling the geometrical continuity and mechanical integrity elements of a joint by creating a complex-shaped structural node that connects to (possibly many) standard structural members in any geometric configuration by using simple standard joining methods. The standard joints between the structural member and the node can be analyzed and qualified by established methods of stress and failure analysis. The body of the node then enables the complex geometric continuity. While it has a complex shape itself, the parametric design technologies BAÑÓN and RASPALL have developed allow it to be generated in an automated way that can control stress concentrations while imparting an appropriate aesthetic quality consistent with the overall architecture. While the shapes are complicated, 3D Printing allows their fabrication as a homogeneous solid which then can also be analyzed and qualified by methods of 3D stress and failure analysis routinely used in various engineering fields.[6_Foreword]

Much research and development remain to be done across all of the elements of the digital design and manufacturing workflows as well as with the workflows themselves. This spans multiple fields, including design algorithms and technologies, new 3D Printing materials and processes for faster, more consistent printing, failure analysis in complex 3D-printed geometries and materials, and optimization of supply chains for the manufacture and assembly of large-scale architecture. All of these, when integrated into seamless digital workflows, will unlock unprecedented innovation in mass customized architecture and product development. It is inevitable that this will happen. As it does, 3D Printing Architecture will be recognized as a catalytic contributor to its happening.[6_Foreword]

Architectural design progresses in tandem with improvements in material technologies. Today, 3D Printing technologies deliver faster, bigger, stronger, and cheaper outputs. Novel workflows from the early concepts to subsequent project development, advanced manufacturing processes, and integration into fully functional products become available. The integration of parametric modeling with performance optimization in the design process is redefining the design process, as the material is computationally allocated where it is the most needed. As a result, forms are efficient and geometrically more intricate. Hence, 3D Printing becomes indispensable by enabling the manufacturing of these intricate artifacts where other well-established technologies fall short.[6_1-11]

With 3D Printing, bespoke forms and multi-functional parts bear the same cost as standard ones; hence, complexity becomes inexpensive, and intricacy can appear at a very conceptual stage. An entirely new set of design opportunities, spanning from extreme levels of precision to minimal tolerances and seamless transitions between printed and standard non-printed components, requires the use of custom-built software and dynamic parametric models to conceptualize and advance a new conception of architecture.[6_1-11]

As a group, these projects explore real examples of how additive manufacturing connects to and expands contemporary architectural trends such as freeform design, computational optimization, ornament, sustainability, and integration of systems. In addition, they elaborate design workflows, covering parametric modeling, optimization, file-to-factory manufacturing, and complex assembly sequence design. Individually, the projects engage on the specific topics of structural optimization, material selection and transition, mechanical properties, manufacturing process, logistics, and assembly procedures. Figure 1.1 exhibits a collection of built designs.[6_1-11]

1.1.1 Expressionist Trend: Formal Complexity

The development of parametric modeling software made the creation and precise control of complex geometries available to architects. Software originally tailored to computer graphics animations and car and aerospace design was applied to the design of physical spaces. From freeform NURBs surfaces to complex part assemblies, the parametric computer-aided design provided a platform to control increasingly complex projects. However, with an exponential increase in the number of unique parts, manufacturing and logistics of projects became progressively more challenging. In architecture and construction, computer numerical control fabrication (CNC), primarily CNC routing, became the go-to solution for complex geometry projects.[6_1-11]

For the manufacturing of complex geometry projects, 3D Printing offers new realms of possibilities. Not limited by subtractive methods, where times and wastage can quickly become immense, additive manufacturing can accomplish true freeform projects with little formal constraints and reduced waste.[6_1-11]

1.1.3 Performative Trend: Structural Optimization

Structural modeling software, once accessible only to specialized engineers, is becoming more accessible and compatible with modeling tools familiar to designers. Therefore, the collaboration between design and engineering gets more fluid and dynamic. Kara and Bosia build this argument through the concept of design engineering [3]. The integration of structural modeling into parametric design modeling tools enables the development of generative models in which designs are automatically adjusted to enhance structural performance. Optimized structures are highly efficient, but often, at the expense of increased geometric complexity. As structural requirements continually change throughout a structure, the geometry and topology of optimized projects reflects these variations with highly differentiated and non-standard components. 3D Printing is an ideal technology for structurally optimized projects because it can achieve complex geometry and bespoke components without increase in cost and manufacturing effort.[6_1-11]

The direct benefits of additive manufacturing in conjunction with data-driven digital models also contribute to other environmental issues, such as reduction of material consumption, wastage, water usage, and emissions. From this point of view, additive manufacturing can contribute to achieving a circular economy model. The development of parametric modeling tools with energy modeling functionalities brings environmental information to designers during their design stage and ultimately improves building’s performance [5].[6_1-11]

This argument is often presented by proponents of Building Information Modeling (BIM), stating that BIM can integrate technical information at an early design stage [6].[6_1-11]



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

The experimental 1:1 material prototypes and new design workflows by architect David Benjamin of the New York-based design practice, The Living, use real-time data for feedback into the design process. The studio has a range of projects and scales, all of which explore human relationships to our environment in different ways. Benjamin builds low-cost sensors, develops custom software and collaborates with artists, material researchers and software developers in his work to gather and utilise new kinds of environmental data.[2-7]

Prototypes have been developed using a thin transparent membrane surface with shape memory alloys, so that the materials contract along its length when electricity is passed through it. The result is a transparent film, and when you breathe into it, it gives the effect of breathing back[2-7]





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

[2-12]通篇

[2-15]通篇

ZHACODE, the research group at Zaha Hadid Architects (ZHA), uses bespoke design tools to ‘sketch with performance’—that is to say, through the creation of custom design tools, the architects can immediately interact with a model to make informed decisions on customisable aspects of building performance.Both the ZHACODE group, and the wider office, consider aspects of performance at a variety of scales in their projects. The office is known for the concept of parametricism, whereby all elements of a design can be seen as interlinked constraints in a computational design process. Developed by ZHA director Patrik Schumacher, parametricism exists because of sophisticated techniques such as scripting and parametric modelling, that he sees are becoming the new normal in contemporary practice. Schumacher writes that ‘one of the most pervasive current techniques involves populating modulated surfaces with adaptive components … components might be constructed from multiple elements constrained/ cohered by associative relations so that the overall component might sensibly adapt to various local conditions’. In parametricism, through computational techniques ‘forms are the result of lawfully interacting forces’.(2)[2-17]

### 数据收集
Data collection is becoming easier, with data supplied from personal devices and other small wearable devices. It may be too easy nowadays, I have experienced projects where people jumped into data collection without much thought on what they want to know, and realised afterwards all the data they collected was rubbish. I see the future to be more data-driven, feedback-based design—ongoing evaluation and iterative/adaptive design to archive the desirable outcome (14).[2-7]




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

[2-18]通篇


## 结论与讨论

## 参数化

In the next decade automation will move the subject of computers in design way beyond the computer graphic narratives (computer-aided design ( CAD)/building information modeling ( BIM)/ parametric) that
have dominated architecture and engineering in the past two decades.[9-1]

Software metaphors such as computer graphics and parametric systems are considered in design theory of computer sciences as the most primitive stage of artificial intelligence.[9-1]

[9-2]
Three Parametric Paradigms

As 3-D parametric software and tools are being rediscovered by architecture and engineering firms, they are beginning to change their design workfl ows. Contemporary design practices have developed at least three different narratives with regard to parametric design:

Parametric formalism: Parametric modeling and scripting has been used by a large number of digital avant-garde designers in intricate complex formal compositions [8]. Designers using this narrative use parametric techniques to substitute the manual designer in form-finding functions.[9-2]

Recently, however, computers and parametric modeling platforms are allowing designers to manage and engage with some of these forms of complexity in ways that have never been possible before. In particular, computationally driven strategies for conducting searches of large design spaces and for capturing complex systemic relationships are beginning to emerge within the design professions. Not only do these types of tools allow for better management of the complexities of our design problems, they can even be leveraged to drive those design processe[9-5]

Computation: The above lends itself quite well to parametric design enabling the use of different types of tools efficiently. This included using various packages like Grasshopper, Digital Project ( CATIA), Tekla, Inventor, and the use of SolidWorks, among many others. This allowed direct data extraction from the digital models and feed into CNC machines for fabrication and then into topographic survey machines on site for installation. Over 15 different software and packages were used by various parties to develop and deliver their scopes. [9-6]

The Al-Bahar Tower’s project presented several remarkable opportunities for parametric design, nonlinear optimization, and kinematic simulation, particularly in the mechanical design of the sophisticated Mashrabiya system.[9-6]

“We began with a full parameterization of the model, which allowed us to compare various stochastically optimized global forms for their relative envelope area to volume ratio, and thus their environmental performance.[9-6]

Adaptive Principles Optimization, Construction, and Performance Manual[9-6]

### automation
Today algorithms, scripting, robots, digital manufacturing, and new autonomous workflow systems are once more transforming the meaning of the term automation. [9-2]

[9-2]
The Automation Themes in Architecture and Engineering: From CAD to Parametric

In the 1990s design and engineering companies in the developed world were implementing small computerization themes by introducing software such as computer-aided design ( CAD) and enterprise programs on personal computers (PCs). However, PC technology only affected skill/ manual labor [6]. From the early 2000s the possibilities of doing small automation routines that can script design workfl ows have moved into the forefront. Some architects and engineers began to use parametric software and scripting to develop parametric design processes.

The most basic conceptualization of parametric refers to a 3-D digital model or digital environment associated with knowledge structures, information, performance properties, and automatic procedures that can aid the designer to construct quick scenarios during design. These models can be updated over time through the Cloud and reused.[9-2]

For instance, automation processes with feedback loop capabilities are natural partners to help designers improve the parameter inputs, predictions, optimize scheduling, identify patterns, and coordinate clashes and interferences. This also includes control and monitoring of ineffi cient energy and water systems in a building or even a city.[9-3]

However, the next generation of computational programming will begin to occur inside the automation domain and not in terms of software design.[9-3]

### history
[9-2]
Brief History of Parametric in Architecture

Parametric is not new. Parametric ideas in design modeling were an essential feature of the fi rst CAD program, Sketchpad, developed by Ivan Sutherland in 1962. Parametric was also part of the pioneering CAD systems in the early 1970s such as SSHA, CEDAR, HARNESS,and OXSYS. These CAD systems had particular parametric features that were associated to a particular type of knowledge base to serve particular organizations and building types [7]. OXSYS was the precursor of building design system ( BDS) and really usable computer-aided production system (RUCAPS), which became available commercially in the UK in the 1970s and surfaced with concepts very similar to today’s BIM systems. All these systems had a common vision: to construct virtually a 3-D building by modeling all their building elements and assemblies. They allowed multi-users to manipulate a single parametric 3-D model in which graphic reports and 2-D drawings were mere automatic derivatives created from the main 3-D model. By the mid-1980s a second wave of 3-D parametrically based software, such as SONATA, Refl ex, CHEOPS, GDS, CATIA, GE/CALMA, Pro/Engineer, Solid Works, and many others, achieved a commercial presence. Many of these pioneering parametric programs in the 1980s became standard in industries such as electronics, infrastructures, aerospace, naval engineering, and car manufacturing. However, most practices in the AEC industry preferred to implement 2-D CAD systems in PCs. It took close to two decades for the 3-D parametric model to make a signifi cant comeback in the AEC industry.[9-2]

### future
[9-2]
Post-Parametric Era

Contemporary parametric metaphors found in scripting and BIM are only scratching the surface of a more profound transformation. Parametric allows for the coding of human reasoning. But parametric is still a manual, labor-intensive, and slow process. These systems are based on defi ning a large number of rules. However, anyone that has attempted to describe design processes with rule systems clearly knows that these systems get extremely complex after 50 to 100 variables are included. Parametric will not automate signifi cantly design processes and will only slightly affect the economy of the whole AEC industry.

In Part II of this book we present a diverse array of cases of technologically progressive architectural and eEngineering firms that are at the forefront of this post-parametric era. The narratives of this post-parametric era are not singular or homogeneous, but on the contrary, they are very diverse and expanding every day. The major thread that brings together these fi rms are their questions about how they can further automate their own custom design workfl ows. These firms are moving beyond CAD/ BIM/ parametric modeling and into semiautonomous and algorithmically driven processes across different platforms to carry specific project tasks. Part II moves through a large array of case studies on algorithmically driven building simulation optimization, controlled façade shades, buildings, infrastructure projects, and urban design tasks.[9-2]

## 1.	参数化设计工具界面体验；

## 2.	数据管理、处理及云平台；
In addition, the next generation of platforms will also include personal supercomputer systems and interoperable Cloud service worldwide.[9-3]

It is also available via the cloud, meaning it can be accessed from anywhere.[9-3]

The future of green building automation will be Cloud-computingcontrolled buildings. Cloud-controlled buildings provide the fl exibility to expand wireless infrastructures with sensor-collected trend data and self-programming data analytics algorithms. The Cloud will be where the applications run and where the data is analyzed and acted upon as it arrives. Digital data is changing; we are moving into a world with an ever growing number of data sources. As the amount of the data and the requirement for algorithms that act on the fl y increase, a green BAS cloud will be able to automatically do real-time stream analytics of different variables in seconds and expand itself to accommodate the operation and peak load control needs on any scale from buildings to cities.[9-3]

## 3.	设计空间形式的分析、构建、到优化生成和机器学习；
[10] 目录 Spiraling, packing, weaving, blending, cracking, flocking, tiling.

### machine learning
With learning algorithms we are moving away from manually coding systems to designing systems that learn from experience. We are in the first steps of creating sophisticated machine learning algorithms that develop specifi c intelligence in design synthesis, building simulation, operation, control, and benchmarking[9-1]

[9-2]
Automating Architecture and Engineering via Machine Learning

In computer science, parametric is considered the most primitive stage of artifi cial intelligence ( AI). As will be described in detail in Chapter 17, most of the major automation projects we see today in other industries are part of the second era of AI: the machine learning period. In this second era AI algorithms are no longer designed to perform particular tasks, but they are designed to learn without being explicitly programmed to do that task.

Machine learning algorithms are deployed to learn from data. They discover patterns and develop predictive behaviors or models to do particular jobs. In many industries these learning algorithms do tasks like the guiding of automated cars, the maneuvering of robots, or detecting patterns in data. AI algorithms allow apparatuses to perform tasks in real-time without being controlled by remote equipment or human. In Part II we show some extraordinary examples of how fi rms are moving into further automating their workfl ows as we move into post- parametric paradigms.[9-2]

there will be a more complex portion of software with integrated high-speed machine-learning and data analytics algorithms that automatically translate in real time new models into executable software.[9-3]

[9-10]通篇
Automating Design via Machine Learning
Algorithms

Introduction

Part II dealt with a large number of narratives from architects and engineers who are automating their processes. These cases are extraordinary and are today at the forefront of practice. The cases presented clearly show that in this post-parametric era algorithmic thinking has moved designers into making higher-level decisions about how to automate their design workflow.

This part will try to answer the following questions: What is next? Which computing methods could further automate signifi cant parts of architectural and engineering design processes? By automation we do not mean the development of systems that imitate what humans do today but we imply the creation of new methods that can signifi cantly augment and renovate contemporary design processes.

Limitations of Parametric Systems

In design theory in computer science parametric systems are considered the most primitive and archaic stage of artifi cial intelligence ( AI). In a parametric system an expert, a programmer, has to manually code all the parameters. Anyone that has dealt with parametric environments knows that major workfl ows in design are an extremely hard, if not impossible, task-to code. The more factors or rules you include in a parametric model the exponentially more diffi cult it becomes to bond design associations.

Today a signifi cant number of narratives about automation deal with the concept of parametric or ruled-based scripting. These narratives have been developed with some success in a number of areas. However, these endeavors are limited and are far from fully automating major architectural and engineering design workfl ows in the AEC industry. Those that optimistically advocate parametricism imply that the more parameters are programmed into a digital environment the more automated the design process will became. They project linearly that if they can code with parametric tools the design of a façade, a series of panels, or a detail today then it is just a matter of time before all types of design and construction information could be manually coded into a universal parametric model.

In this chapter, we put forward the idea that at present we are well into a second era of AI. In this new age, machine- learning algorithms can perform automated tasks by being trained from previous data. We suggest that these computing methods will be highly infl uential in the next generation of automation of design in the AEC industry.

Algorithms vs. Learning Algorithms

There is a difference between an algorithm and a learning algorithm. An algorithm is a set of instructions to perform a particular calculation or procedure. A learning algorithm is a set of instructions for a computer to learn from data and perform an action without the assistance of a human. Today learning algorithms that have been trained to detect traffi c signs double the performance than that of humans. A whole generation of diverse products, including Internet search, automated translation, forecasting energy production, the driverless car, automated trading, drug design, and fraud detection are the results of learning algorithms.

With learning algorithms we are moving away from manually coding systems to designing systems that learn from experience. We present at the end of this chapter an example of how this could be possible between the framework of architectural design with a method that automatically generates programs, 2-D fl oor plans for residential buildings, and 3-D models in different architectural styles—100,000 iterations of 2-D fl oor plans in 35 seconds. We fi nally discuss why parametric is a limited paradigm for the future of design automation in the construction industry.

Computers as Autopoietic, Self-Organizing, and Self-Learning Systems

Terry Winograd and Fernando Flores wrote a book in 1987 called Understanding Computers and Cognition: A New Foundation for Design [1, 2]. Winograd is a highly infl uential AI professor at Stanford who was also the Ph.D. advisor of the doctoral thesis that was converted into Google. The book has proven to be deeply infl uential in computer design, however it is hardly known in architectural or engineering design circles. The book was written in a period in which AI was highly discredited.

The book works on developing a new understanding of what intelligence and cognition mean in the context of designing computer systems. The authors discredit the rationalistic approach used in AI during the 1980s. At that time, AI was heavily based on formal representations of intelligence such as rules, knowledge bases, and operations that describe intelligence in very narrow terms.

Instead the authors are inspired by the concept of autopoietic or selforganizing systems developed earlier by biologists Humberto Maturana and Francisco Varela [3]. These biologists argued that living organisms have extraordinary design intelligence because they self-organize by learning from their environments and they are not planned from the exterior.

Winograd and Flores criticize the old rationalistic software design because they create intelligent systems that are programmed by an outside coder, thus are not self-organizing or autopoietic. They concluded at the time that new approaches for designing computer systems were needed and put forward the notion of computer systems that somehow learn by themselves from their environment and self-organize. Winograd and Flores put forward the notion that the design of AI systems would come in three different stages of computer learning:

1. Parametric;

2. Machine learning;

3. General AI.

Parametric: First Stage of AI

In the fi rst and most prehistoric stage of AI one can fi nd parametric systems that via parameter adjustments or combinatorial search do basic intelligent operations. Winograd and Flores mention that after a short-lived peak in the 1950s and 1960s this type of work has been almost fully abandoned in the computer science community. Parametric allows for the coding of human reasoning; however, it always requires the hand of a coder that is expected to be able to observe all the potential steps of every condition of intelligent behavior.

Contemporary parametric endeavors in the design of buildings are good examples of the fi rst age of AI in the architecture and engineering domain. This fi rst age has allowed architects to make more explicit their design processes, but most of these systems are not self-organizing or autopoietic. These parametric systems can usually only tackle a few parameters. They are usually used in very particular evaluations but cannot fully automate large workfl ows of design processes.

Machine Learning: Second Stage of AI

A second level of AI impacts occurs when computers perform concept learning and concept formation. Here algorithms learn from data. These learning algorithms fi nd patterns in data and build probability or predictive models for a specifi c job. Today learning algorithms work in a large array of tasks, they are usually very specifi c, and the techniques have spread rapidly in the computer science discipline.

Arthur Samuel, one of the early pioneers of AI, described machine learning as the “fi eld of study that gives computers the ability to learn without being explicitly programmed” [4]. Automated learning systems learn from information using techniques such as artifi cial neural networks, decision tree learning, support vector machines, Bayesian networks, Boltzmann machines, and deep learning, among many others.

Machine learning algorithms can be classifi ed into several types depending on the desired results and data available. They can be categorized as supervised learning, unsupervised learning, semisupervised learning, reinforcement learning, learning to learn, or transduction.

Today, learning algorithms are everywhere. They are automatically selecting companies for venture capital fi rms, and they are automating the discovery processes of many large practices in the legal community. Complex algorithms are already replacing engineers in certain tasks of chip design, writing sport news, Web articles for Forbes Magazine, grading English essays, developing patrol routes for the Los Angeles police, and are at the core of the IBM’s Watson supercomputer that beat two former human champions of the TV game Jeopardy! after just 2 years of training.

Examples of Machine Learning Algorithms Outside the AEC Industry

An example of supervised learning is a driverless car that is trained how to drive by creating a neural network system that captures images of the road, 3-D laser data, and at the same time records the steering directions of human drivers. Once the system is trained the car will capture images and 3-D data of the road as the car moves, and the steering direction will be controlled by the neural network optimized results.

Another example of learning algorithms is automated translation similar to Google Translate. A translating system developed with parametric techniques will require that the programmer manually code all meanings and double meanings of words from one language to another. Just a single word can have a vast array of meanings, which makes translation by parametric means an impossible task. Machine learning algorithms do not understand text but if they are fed two texts in two different languages they will be able to parse the text and detect probability patterns such as that every time the word “one” appears in English then the word “uno” shows up in the Spanish text. Complementary algorithms can further aid the process by creating phrase tables to help assure the particular meaning of a word or sets of words. The more text is fed to the algorithm the higher the certainty that the predictive model will fi nd the right translation.

Learning Algorithms in Architectural Design

Machine learning algorithms in the architectural design domain can evolve in several directions. In Chapter 10, Lars Junghans describes in detail the direction toward “ automated building optimization algorithms.” Another subject that has deserved signifi cant attention in the architectural domain has been the automation of fl oor plan design in the initial stages of a project. A large number of attempts can be traced back to the 1970s, including the work of Per Galle [5], Bill Mitchell [6], shape grammars, heuristic optimizations, or contemporary 3-D parametric modeling and scripting. Most of these previous approaches are rule-based systems that adjust particular arrangements. But none are able to fully automate the design synthesis process from creating automatically a program, 2-D plans, or 3-D models.

The most advanced method in the area of automation in design synthesis can be found in the research led by Stanford professor Vladlen Koltun, whose work has been focused on visual computing and design synthesis using machine learning. These systems are not programmed with rules but are trained by feeding them a list of data sets such as shapes, program, size, and adjacencies found in the real world. The learning algorithms of this Stanford group have allowed for the automated generation of the architectural program, fl oor plans, sections, and 3-D models based on data feed from a book using machine learning techniques.

Automated Design for Residential Building

In 2010, Vladlen Koltun with Paul Merrell and Eric Schkufza guided the completion of a method for automatically generating the spatial design of residential buildings with a complete automated generation of architectural program, fl oor plan layouts, elevations, and 3-D models. The methodology used a Bayesian network. A Bayesian network is a type of statistical model that represents the probabilistic relationship between variables and conditional dependencies—a highly popular method in second generation types of AI endeavors.

This Bayesian network is trained on existing residential housing data found in the book Essential House Plan Collection by Hanley Wood [7]. From that data the network produces an architectural program without human intervention. From the generated building program the team uses a stochastic optimization to automatically generate sets of fl oor plans. From  the plans entire 3-D buildings are generated in different styles that were also extracted from the book (Figure 17.1).

Automating Building Layout Design

The automation of fl oor plans has received intense interest since the 1960s. These endeavors have ended up in hundreds of methods that have resulted in numerous prototypes that have not truly automated the complete building layout process [8]. Most of those early endeavors programmed algorithms that tried to formalize design rules, criteria, and relationships manually, but none of them truly automated the process.

Koltun and his group at Stanford studied how three residential architecture fi rms developed building layouts in practice. They observed that the architects entered into a very time-consuming iterative process that include the construction of bubble diagrams, adjacencies, program lists, and multiple concept drawings that attempted to match the room requirements in different fl oors. In 2010 they noted that “real-world architectural programs have signifi cant semantic structure.” For example, “the presence of three or more bedrooms increases the likelihood of a separate dining room” [9].

They argue that these types of relationships are vast in the architectural domain. For them it is not clear how the implicit knowledge found in the architectural practice domain “can be represented with a hand-specifi ed set of rules or with an ad-hoc optimization approach. A data-driven technique is therefore more appropriate for capturing semantic relationships in architectural programs” [9]. Thus, instead of using a ruled-based system this method trains a Bayesian network with data obtained from the book.

The automation of this building design methodology is a three-step process: (1) The generation of the architectural program, (2) the automatic generation of a set of fl oor plans, and (3) the automatic generation of a 3-D model. Figure 17.1 and also a short video of their 2010 published paper clearly shows the process followed by this method [10].

I. Automatically generating architectural programs with Bayesian networks. The objective of the fi rst step of this method was the training of a Bayesian network with real-world architectural data. To nourish the system the team at Stanford manually coded architectural programs that were selected from  120 projects from a popular book about residential design [7]. Features from every room of these 120 residential cases were recorded. The features tabulated included the program type, square footage, aspect ratio, adjacency, and other aspects that traditionally mediate the relationship among the rooms such as doors or open-wall connections. An example is shown in Figure 17.2.

The network-structured learning discovered a large number of relationships that were present in the data. For example, a room type such as a bedroom is an excellent forecaster of the room’s size and aspect ratio. From this data the Bayesian networks can generate specifi c programs after 10, 100, and 1,000 iterations (Figure 17.3).

II. Automatically generating 100,000 fl oor plan iterations in 35 seconds. The second phase involves turning the architectural programs generated in the fi rst phase into entire fl oor plans for each fl oor. Several techniques are used to align walls and rooms. Figure 17.4 illustrates several ill-formed fl oor plans that do not comply with a set of specifi c terms such as accessibility, area, aspect ratio, or shape that were introduced to improve the quality of the fl oor plans. Figure 17.5 shows the fl oor optimization process from 200 to 100,000 iterations that “took 35 seconds using an Intel Core i7 clocked at 3.2GHz” [9], similar to a typical processor found in a desktop or laptop computer in 2014.

III. Automatically generating 3-D models. From the building layouts generated in the second phase the team created 3-D models in different styles based on style templates that list the “geometric and material properties of every building element: windows, doors, wall segments,gables, stairs, roofs, and patio poles and banisters” [9]. Figure 17.6 illustrates four 3-D models in the cottage, Italianate, Tudor, and Craftsman styles that were automatically generated for the same 2-D building layout. The styles were extracted from the Hanley Wood book [7].

The work directed by Professor Koltun at Stanford is a highly sophisticated machine learning methodology applicable to the architectural domain. A more sophisticated type of method can be developed by training the machine learning algorithms to become skilled at styles or design concepts found in a diverse population of work and designers. Style, in a creative realm, is a higher-level semantic problem found in design. Initial ground has been developed in drawing and painting learning algorithms [11] and will certainly continue to evolve in the creative domains.

Machine Learning Hardware: Neuromorphic Processors

Most of the explosive advances in the machine learning fi eld in the past decade has occurred in software design. However, the hardware of computers has remained very much related to the digital computer architecture that emerged from the mathematician John Von Neumann around 1945. In very simplistic terms the Von Neumann model is a device that can calculate at very fast speed using strings of 1s and 0s. Today’s machine learning algorithms usually have to represent, evaluate, and optimize data in a calculable format that a Von Neumann computer can handle. Thus, a signifi cant part of machine learning efforts to date has been based on statistical-oriented algorithms that employ brute force, using massive computer power to perform a colossal number of calculations on a huge number of data sets.

Biological organisms are much more effi cient in developing intelligent behavior than contemporary computers. There is an emerging fi eld in hardware design that is developing neuromorphic processors that allow us to create a machine that truly learns by experience. Neuromorphic computer processors have an architecture that imitates the neurobiological design present in the nervous system of organisms. These electronic circuits are connected by wires, and their overall design mimics the morphology of neurons and biological synapses. Initial prototypes such as the ones sponsored by the DARPA SyNAPSE program at IBM and HRL Laboratories, Neurogrid at Stanford [12], and several projects under the sponsorship of the Human Brain Project (HBP) in Europe show early glimpses of computable brain simulation for tasks such as visual recognition, edge detection, music identifi cation, pattern recognition, color identifi cation, or smell. For example, a system of 120 neurons from HRL lab learned how to play the game Pong after fi ve rounds of playing with the paddle and sensing the ball from the game. The system was not programmed; it only received feedback via rewards for a good job or punishment for a failure.

Neuromorphic systems will be complementary to today’s computers whose capabilities continue to grow explosively. Several companies are announcing the commercial release of neuromorphic systems in 2014. They represent the next generation of technology that can move us closer to a third stage of AI systems.

General AI: Third Stage of AI

A third generation of AI will emerge when a device is no longer programmed but evolves and develops primarily by learning and can produce other machines even more intelligent than itself. Computer power and technology today is far from achieving the third stage of AI. But according to authors like Ray Kurzweil, now head of the Google mind project, by 2029 computer power will allow us to reverse engineer the human brain, which will be a signifi cant advancement to create computers that learn by themselves [13]. Others like Jeff Hawkins, cofounder of the AI company Numenta, which has created some of the most sophisticated learning algorithms that operate like the neurons in the neocortex part of the brain, say they are very doubtful that this third stage will ever be achieved. In the meantime, at least for the next two decades, we are bound to observe the explosion of machine learning algorithms and hardware that are affecting many domains and industries.

Conclusion

The intention of this chapter was to place the automation efforts of the architecture and engineering community in context with the contemporary discourses of design theory in computer science today. We have put forth concrete examples about how machine learning is entering the domain of design. Machine learning algorithms are also entering into many others aspects in the construction industry such as BAS, procurement, and sensors systems.

Still there are doubts whether learning algorithms and neuromorphic processors could scale up to truly imitate the sophistication of biological systems. The subjects of AI, machine learning, and deep learning will continue to expand as computer power grows exponentially. There will be big AI booms and also major busts along the way. The second generation of AI learning algorithms are transforming many aspects in many industries and as illustrated in this chapter will also impact the construction industry in this post- parametric period. The major limitation is that there is very limited expert knowledge in learning algorithms available in the design community, which is the reason for the narrow use of this method in the AEC industry today.[9-10]

### generative design/genetic algorithems
For example in one approach they used self-organization-based agent models with attractrepel algorithms in which a user can interactively generate space planning and quick massing studies. Other methods include urban spatial planning, access design, and occupancy and behavioral mapping. The chapter emphasizes that architecture is meant to provide experiences by using spaces and observes that digital design procedures should be able to help generate, visualize, and evaluate the heuristics of places and users.[9-4]

Another search technique being used on design problems is the genetic algorithm ( GA). With a GA, the designer must fi rst characterize the design as a series of numeric variables that correlate to the geometric properties of the design, essentially its genome. These values are free to change during the course of the algorithm’s execution as it searches for the combinations of values that lead to the creation of the best solutions. Again, the designer must also describe “best” in terms the computer can calculate and measure [9-5]

[9-8]通篇

Generic Optimization Algorithms for Building Energy Demand Optimization: Concept 2226, Austria

Lars Junghans

Introduction

The need for computer software in building planning processes to calculate the performance of a project is self-evident nowadays. Building simulation programs are used to calculate the energy demand, the structural load, or even the cost of a building. 

Building design and renovation projects are multivariable parameter problems that include a large number of possible combinations of parameter settings. The parametric study often used in planning processes involves changing one parameter while leaving others constant. These studies can miss important interactive effects [1]. One way to fi nd a global optimal solution is to use enumerative search methods where all possible parameter settings are combined with each other. Because of the large number of combinations, however, this optimization process is computationally expensive and would take too much time. A more promising solution is to use an automated building optimization algorithm coupled with a simulation program to fi nd an optimal solution [2].

The term “building optimization” refers to an automated method that uses algorithms to fi nd the optimal combination of parameter settings for building design and renovation. The objective of the method is to fi nd an optimum for the lowest energy demand, cost, or greenhouse gas emission. When building design parameters of the building envelope, the building automation as well the HVAC system can be included in the optimization process. The term automated building optimization indicates that the building optimization algorithm provides optimal solutions without extensive user interaction. The user still needs to defi ne the problem and needs to provide necessary material data. A typical future task of automated building optimization algorithms would be to defi ne the optimal properties of a climate-responsive building façade. In this task, the optimal combination of window to wall ratio, glazing, insulation, and shading geometry will be found to reduce the energy demand for heating, cooling, and artifi cial lighting. Automated building optimization will even be able to defi ne the shape of a building within a given building program. In the building sector the goal of a building optimization algorithm should be:

1. Reduction of computation time

2. Robustness of the results

3. User-friendliness of the application of the algorithm.

Reduction of the computation time is especially important for automated building optimization algorithms because they are using time-consuming thermal dynamic simulation software. A calculation time of several hourslike in a multiparameter optimization problem, can be critical in a planning process, especially in the early design stages.

The robustness and reliability of the calculation results in a recommendation of the global optimal solution that is especially important for the user. Some of the current available optimization algorithms are not adjusted for the special needs in building optimization problems, which are different than the needs in other scientifi c optimization problems with a much larger problem space.

The user-friendliness is important for the use of a building optimization algorithm in planning projects where no expert knowledge is available. Some currently available building optimization algorithms need expert knowledge in the use of the algorithm and its connection to the simulation software tool. This often not existing expert knowledge is a reason for the currently limited use of building optimization software in practicing planning offi ces.

In this chapter, strategies are described as the elements in a search space. Each strategy has a combination of parameter settings. To defi ne the performance of each strategy a thermal building simulation is necessary. In general, optimization approaches taken toward achieving the objective described above can be classifi ed as discrete and continuous parameter optimization methods.

Discrete parameter methods are mostly used for building optimization. For example, a fi nite number of available construction types and thicknesses are available when adding insulation to a wall. In contrast, continuous parameter methods do not use fi xed numbers for the parameter setting for building shape or dimension such as the window-to-wall ratio, building orientation, or compactness.

Continuous parameter methods based on numerical optimization were studied as early as the 1990s [3]. Although researchers found that numerical building optimization algorithms based on simulations have nonsmooth functions and can fail to fi nd the optimum solution [4], several optimization methods using continuous parameters have been successfully developed for building shape and dimension optimization. These methods include the simplex method [5], the pattern search algorithm [6], the harmony search algorithm [7], the multidirectional search algorithm [8], and the simulated annealing algorithm. However, even given their theoretical success in fi nding optimal building shapes, these methods are limited because building optimization projects have a combination of discrete and continuous parameters and are not useful for these studies. Instead, optimization methods using discrete parameters, like the genetic algorithm, particle swarm, and sequential search methods, are more suitable.

Optimization Methods: Probabilistic Optimization Methods

1. Genetic algorithm. The GA is a probabilistic search technique for solving complicated problems using evolutionary principles to fi nd optimal solutions [9]. It searches for an optimal solution to a multiparameter problem by simulating the natural selection over generations. A potential combination of parameter settings is described as genes on a chromosome. A population is created in every generation where the performance of each population is expressed in a fi tness factor. Members of the populationa re paired up to create a new generation. The selection for the parents is selected randomly, where members with a better fi tness factor have a better chance to be selected.

As with organisms in nature, a crossover of the chromosomes takes place to defi ne the property of the genes of the children. In some GAs, a mutation process takes place to refresh the gene pool. The process of producing new generations is repeated until an adequate optimal solution is found. The GA is seen to be a robust search technique to avoid local minima. However, with each iteration or generation of the algorithm, a different path toward an optimal solution occurs and the end result may also be different [10].

An advantage of this algorithm is that it avoids generating local optimal solutions, which is a problem with the numerical optimization algorithm. The GA has many practical uses in building science, including the optimization of structural systems, building shape [11,12], and building HVAC [13]. However, experiments have illustrated that this algorithm does not always result in good solutions. Currently, the optimization process must be repeated several times to prove that the recommended solution is the global optimum. This repeating simulation process has the disadvantage of extending the overall calculation time of the optimization process. This is the reason why the GA has not found its way into practicing planning offi ces.

2. Multiobjective genetic optimization. The GA can be used for multiobjective optimization problems. Rather than only having one fi tness criterion like the energy demand or the life-cycle cost, a multiobjective optimization algorithm will provide optimal solutions for two or more fi tness criteria. The multiobjective GA normally provides pareto-optimal solutions. Researchers have used the multiobjective GA to fi nd optimal solutions for the life-cycle cost and the life-cycle of greenhouse gas emissions.

3. Particle swarm optimization method. The particle swarm optimization method has many similarities to the GA and also proceeds by probabilistic parameter settings [14,15]. However, unlike the GA, the particle swarm method is based on the social behavior of birds or schools of fi sh rather than on evolutionary principles like mutation and crossover. In each iteration step, parameter settings are changed randomly, and strategies, or swarm particles, in the search space are compared to each other. Changes to parameter settings of the most successful particle are adopted by the other particles in the search space. The process is repeated as long as necessary to fi nd the optimum. Although this method has been used successfully for building optimization, the method has been found to be more computationally intensive than the GA [10].

Optimization Methods: Sequential Search Algorithms

1. Sequential search algorithms. A sequential search algorithm is a top-down optimization method that iteratively improves the building performance. Unlike other optimization algorithms, sequential search algorithms are not based on randomly defi ned parameter settings. In each iteration step, the most effective solution is found by comparing the results of previously defi ned strategies and parameter settings. The process is repeated until an optimal solution is found. A vector path is found from the initial design of the building to the optimal combination of parameter settings. The optimal strategy in the search space is found according to its marginal benefi t and recorded in each iteration step. Because of this sequential approach,this algorithm has a signifi cant advantage over optimization algorithms that provide only the optimal solution in that it ranks the recommended strategies and also provides the marginal benefit.

A difference in the sequential optimization process, or greedy search, used for building simulation compared to the problems in microeconomics or mathematics is that the starting values, such as energy demand or lifecycle cost, will change dynamically in each iteration step in relation to reductions in operation energy demand in each successive step. Only topdown sequential approaches can be used because forecasting the results in future iterations is not possible. Thus, there is a risk that large improving strategies can be overlooked in earlier iteration steps.


2. Equimarginal optimization. The equimarginal optimization algorithm (EO) is a sequential top-down algorithm that solves the problem of the greedy algorithm and uses concepts from microeconomics [16]. As background, marginal utility (MU) is the benefi t or satisfaction from the purchase or consumption of a selected quantity unit of a good or service.

The EO is based on the diminishing marginal utility that is the effect when the MU decreases with the increasing quantity of a good or service. The EO has the advantage compared to other building optimization algorithms that it provides the marginal benefi t of the investment for each possible recommended strategy. It also ranks the recommended renovation strategies according to their reduction of energy demand or life-cycle cost Architects and decision-makers are thus able to fi nd the balance between the long-term life-cycle cost and the short-term investment. Because the EO is a top-down search method, it has its advantages in building renovation projects, where a nonrenovated building with high energy demand will be improved.

Available Optimization tools

1. GenOpt. GenOpt is an optimization tool developed by the Lawrence Berkeley Laboratory in 2001. It is based on the Nelder-Mead pattern search technique, which is a special form of the simplex method. The algorithm needs concave functions in its parameter-setting description. GenOpt can be used as an optimization platform for simulation software tools like EnergyPlus or TRNSYS. Researchers have used GenOpt for building and system optimization where concave functions of the parameter settings are available. So far, expert knowledge is necessary to integrate GenOpt in simulation software.

2. BEopt. BEopt is based on a sequential search algorithm and is a version of the greedy search technique. It uses the DOE 2 and TRNSYS as a simulation environment. For each iteration, the most cost-effective strategy is chosen based on the reduction of life-cycle cost. As in most forms of sequential search algorithms or the greedy algorithm, the chosen strategy is then removed from the parameter search space for future evaluation. The developer of BEopt modifi ed the algorithm to overcome the problem of overlooking large improvement strategies and negative interactions between strategies. BEopt keeps track of solutions in previous iterations and compares them with the current solution. Interactions between parameter settings must be identifi ed by the user before using the algorithm so technical expertise is necessary [10].

3. Genetic algorithm. A number of free available optimization tools are available that are based on the GA. These tools are mostly based on computer language codes like Java, C++, or Python. The MATLAB program also has a number of GAs in its library. All these tools require expert knowledge in the use of the optimization algorithm. Additionally, computer coding is necessary for their use in building optimization.

Future Developments in Generic Building Optimization

1. Improvement of usability in the architectural praxis. Current optimization algorithms need expert knowledge for their use in building optimization. Future building optimization algorithms should be adapted to the needs of building optimization. A goal must be to develop optimization algorithms that can be used by architects and planners without expert knowledge in optimization theory and computer science. The robustness of the outcome of a building optimization process must be improved so that the user can rely on the outcome of the process.

2. Improvement of the calculation time. Large energy reductions in the built environment can be achieved in early design stages in the planning process. When a building is designed or renovated, it is often not clear which part of the building envelope or technical system is most effective to renew, improve, or replace. To meet these requirements, the algorithm used in the early design stages must feature a short calculation time to meet economical aspects. The following calculation methods currently exist and will be discussed in the following sections: static calculations,
dynamic calculations, and climate surface calculations.

Static calculation methods that appear in national building codes are based on simple equations with a limited number of values representing the specifi c climate. An advantage of these methods is that they do not have a long calculation time. However, these methods do not consider the time correlation of outside air temperature, solar radiation, internal thermal mass, and internal heat gains. Therefore, the imprecise results of the static calculation cannot be used for building optimization. 

Dynamic calculation methods using dynamic simulation software programs such as DOE2, EnergyPlus, and Trnsys have been introduced into the scientifi c community. The programs calculate the energy demand in short simulation time intervals of an hour or shorter based on hourly weather data of a reference year. Unlike static calculation methods, advantages of these dynamic methods are that they consider time-correlation, are more precise, and consider different qualities of the built environment. However, the programs are too time-consuming because they are based on a large number of thermal dynamic calculation processes in each iteration step.

Burmeister and Keller [16] introduced a concept called the climate surfaces. Dynamic presimulations are necessary to generate the data matrix for the climate surface of a specifi c building type. This fast-calculating method can overcome the disadvantage of the computationally expensive dynamic simulation tools. However, the climate surface method needs to be extended with factors like natural ventilation, daylight, shading, and psychrometrics.

3. Clarifi cation of uncertainties in building optimization. The GA and EO derive their usefulness in building optimization through the use of thermal dynamic simulation tools for energy demand predictions. These tools are based on a vast set of climate data and can thus produce accurate predictions, which is critical for sustainable and economic building evaluations. However, life-cycle assessments for greenhouse gas emissions and costs in building science commonly suffer from signifi cant uncertainty due to lack of information. Uncertainties occur as a result of differences between the physical reality and the simulation calculation model [17], cost defi nitions [18], and defi nition of the specifi c environmental impacts of building material and systems. Because of these uncertainties, the proposed optimal solution given by computer-based building optimization can create unreliable results [19].

For building planners, designers, and project decision-makers, it would be very helpful to be able to quantify the uncertainties of the results in a building optimization process. Depending on the assessment criteria, an option with a smaller predicted return and a smaller risk might be preferred to an option with a larger predicted return and a larger uncertainty or risk. When information is severely uncertain, a decision-maker may want to make a decision that will yield a reasonably satisfactory result over a large range of realizations of the uncertain parameters.

Conclusion

Automated building optimization algorithms and systems are becoming more and more useful in architectural design processes. Great energy use reductions, cost reductions, and greenhouse gas reductions are expected by the use of these generic software tools. By the integration of faster calculating simulation tools, optimization processes will be applied by architects in early design stages.

In the near future, architects will be able to design buildings and building elements with a higher confi dence in optimal solutions than in the past. Results will be presented as continuous values, including the mean value, expected value, and the deviation. An improved risk management will be possible. It will be up to the architect or decision-maker to decide how far an automated building optimization decision support system will go.[9-8]



## 4.	结构分析、构建与设计空间形式协同优化；
Genetic algorithms are used in performative searches for structural and environmental control solutions and metrics.[9-4]

In Chapter 7, Lucio Blandini, Albert Schuster, and Thomas Spiegelhalter illustrate how a large-scale infrastructure project is designed, coded, and scripted through a highly automated workflow process of nonlinear analysis and structural behavior optimization methods. Scripting was hereby a very helpful method for the automated modeling and optimization of all the workfl ow scenarios between the different professionals involved. Besides the structural optimization, the project was also algorithmically modeled to discover the most effi cient low-energy scenarios and assembly strategies. Compared to an average railway station structure with the same spans, this team was able to reduce the overall structure to one-hundredth of span, resulting in the use of much less material. The new zero-energy railway station is discussed as a prototype of a new generation of railway typologies that will provide passenger comfort with passive strategies on the highest level.[9-4]

Figure 3.1 Optimal truss research: This series of images reveals the optimal structural form for a truss, given a specific set of loading, restraint, and meshing criteria, generated using a force-density algorithm.[9-5]

An ongoing research initiative in our structural engineering studio is exploring the concept of effi cient truss topologies. One strategy being leveraged in this exploration is an optimization method called the force-density method. In this search technique, the solution space is a somewhat arbitrarily defi ned block of material with explicitly defi ned supports and applied loads. The search algorithm works like a sculptor, iteratively removing pieces of the block of material that are doing the least amount of work in the transfer of the forces from the loading points to the supports. The result of this iterative subtraction process is a truss form that corresponds to the most effi cient use of the available material; in other words, a structurally optimal truss. If the loading or support conditions are changed, the resulting form will be changed as well. [9-5]

With built-in palettes of NURBS-based shape generation tools, geometry modeling programs like Rhino, Grasshopper, and Digital Project have made it relatively easy for designers to create building shapes that are highl complex and curvilinear. These complex curvilinear geometries must then be rationalized into curtain wall cladding systems, generally consisting of quadrilateral panels of glass and aluminum framing systems. Additionally, the structural systems (including the fl oor slabs, perimeter columns, and substructural components) that hold up the curtain wall system must also be rationalized to refl ect the surface geometry of the building. [9-5]

It was recognized at the start of the project that a parametric design process was necessary to effi ciently analyze and document the buildings while still providing freedom for variation within the design. Cox and Arup collaborated to construct the parametric model using Rhino and its parametric design plug-in, Grasshopper. The architect set up and controlled the components that generated the overall shape of the building and the centerlines of the portal frames, while the engineer dictated the required structural properties and performed topology and section optimization. A script was developed to generate the structural framing of the halls from the architectural input with minimal adjustment.[9-7]

## 5.	可持续性设计及设计空间形式协同优化；
### Carbon
The targets for carbon neutrality can temporarily be accomplished through interoperable parametric-algorithmic design optimization processes to predict the future of the operational resource use of buildings. These design workfl ows also incorporate total life-cycle scenario tools for performance, material properties and resource use, and design-to-factory procedures. The intended interoperability for these building information model ( BIM) platforms is the capability of autonomous, heterogeneous systems to work together as seamlessly as possible to exchange information in an effi cient and usable way. The advantage is described that these 3-D- BIM design platforms links variables, dimensions, and materials to geometry in a way that when an input or simulation value changes, the 3-D/4-D/5-D model automatically updates all life-cycle scenarios and components simultaneously.[9-3]

Today and in the future, automated green building manufacturing will go naturally together with faster and more flexible customization, and corporate sustainability strategies to reduce manufacturers’ carbon footprints and energy costs for revenue growth with return on capital employed (ROCE).[9-3]

### BAS building automation systems
Today’s building automation systems ( BAS) are centralized, interlinked, and sensor driven human-computer-interface (HCI) networks of hardware and software. They monitor, control, and optimize in real time the environment in residential, commercial, industrial, and institutional facilities. While managing various building systems, the learning automation system ensures the operational performance (transportation, light, water, HVAC, energy generation, storage and distribution, etc.) of the facility as well as the comfort and safety of building occupants[9-3]

### sustainable
Sustainable traditions from the craftsman era that were either lost or underscored during the era of mass production can now be individually integrated in green manufacturing and 3-D printing settings.[9-3]


## 6.	BIM和GIS的参数化途径；
### BIM.
[9-2]
2. Parametric BIM: BIM has become one of the central themes in the computerization of architectural practice today. BIM software and processes allow architects and engineers to construct virtual models that accurately replicate building systems, materials, performance, and lifecycle processes. BIM narratives in practice have mostly concentrated in what the AEC industry calls 3-D, 4-D, 5-D, and 6-D BIM.

3-D BIM refers to collision detection models; 4-D BIM is used for construction sequence models; 5-D BIM models are associated with cost estimation; and 6-D BIM models are used for facilities management during the life span of the building. The merging of these parametric BIM models with embedded sensors procurement procedures, building simulation modeling, intelligent 3-D libraries, price engines, and bidding systems will move the narrative further. However, in spite of the exaggerated claims in the media that BIM is “revolutionizing” the AEC industry, BIM is still a labor-intensive procedure, and it is not a radically more intelligent method.[9-2]

Some of those interoperable BIM platforms allow free plug-ins for several CAD tools (Graphisoft, ArchiCAD, Autodesk’s Revit Architecture & MEP, Rhino, SketchUp, Grasshopper, Bentley, etc.).[9-3]

### GIS 



## 7.	机器人建造与3D打印；
architects and engineers are developing custom fabrication and mass customization techniques by developing in one case a large number of subassembly units just-intime and in another case using robotics to achieve very unique design performance and life-cycle design quality.[9-1]

Today we have experienced only 3-D digital manufacturing platforms such as 3-D printing, computer numerical control ( CNC), laser cutting, and infl exible robotics. 3-D digital manufacturing alters materials on a large scale. We are quickly entering into a 4-D digital manufacturing period in which we will be able to design, create, and print all sorts of new environmentally sound materials at a microscopic level, inventing materials that cannot be found in nature. In a longer horizon we will began to see the emergence of an N-D digital manufacturing era in which materials can be programmed and be malleable at will.[9-1]

[9-2]
Automating Construction via the Future of Digital Manufacturing The prefabrication and manufacturing automation narratives described in Part III are extraordinary but are by no means the ultimate image of automation in construction. On the contrary, they are just the preparation acts. Chapter 18 argues that digital manufacturing will ultimately challenge not only the way we process materials but also create completely new materials and eventually programmable matter—materials that can transform their physical properties via programmable control. The impacts of digital manufacturing will come in three different stages:

1. 3-D digitally manufacturing any forms;

2. 4-D digitally manufacturing completely new materials;

3. N-D manufacturing via programmable matter.

First, today an array of digitally controlled machines such as 3-D printers, CNC machines, robotic arms, and laser cutters is allowing us to manipulate any construction material with extreme accuracy. However, most of these impacts are at the level of manipulating materials at the human scale, but these changes do not affect signifi cantly the performance of materials. Today we are entering into a 4-D digitally manufacturing era. In this second period we can use multimaterial printers and nanotechnology to manufacture completely new materials that cannot be found in nature. Further into the future a third epoch of N-D digital manufacturing will emerge when we are able to program materials to perform interactively

On the one hand we look at how a large number of architectural and engineering fi rms are transforming their practices by using parametric, BIM, and scripting tools that help them automate parts of their design and analytical routine work from design to fabrication. On the other hand we observe how large engineers/contractors have begun to transform their construction practices by moving gradually into prefabrication, modularization, and manufacturing.

Both narratives are incomplete. The design automation led by architects and engineers using parametric will not succeed in automating a signifi cant number of workfl ows in the AEC industry. Instead, machine learning algorithms such as the ones used in many other industries will allow the design fields to automate their processes in a more effective way than parameter adjustments.

The current trend from engineers/contractors for prefabrication and modularization will potentially encounter the rise of 3-D multimaterials printers and synthetic biology processes. These methods can produce all types of new materials and biomaterials that can be designed at the microand nanometer level to respond to very particular conditions. This will lead to a completely new way of looking at digital manufacturing.

The advent of a more precise way of construction will eventually lead to a transformation of the designer and the traditional design process. Traditional design processes, either via hand-drawing or even with parametric CAD, are unable to plan with designing material performance at the macroscopic and microscopic levels. Machine learning design automation will have to play an increasingly important role in design synthesis for the construction elements that use multimaterials in the near future. As was observed at the beginning of this chapter, automation implies important themes in saving labor, energy, and materials, as well as construction quality, and sustainability. The last factor will be an important factor throughout this book and the subject of the next chapter. The construction sector is in urgent need of modernizing and shifting toward sustainable construction practices as this has been identifi ed by the United Nations (UN) as a key industry in the attempt to solve global warming [11].[9-2]

Real life-cycle requirements can be simulated in various situations, such as ergonomic human-machine interactions, maintenance intervals and shift patterns, or infrastructural resource input and output fl ows. Once a factory is built and in operation, the digital life-cycle metamodel enables users to run optimization experiments and what-if scenarios without disturbing an existing production system of the entire plant. The case study also explains the latest developments for learning algorithms based on neural networks, and wasp swarm optimization of logistic systems and automation in the fi elds of engineering, manufacturing, infrastructure, city, and building automation. In particular it describes how machine learning and adapting mechanisms are used for black box modeling and optimizations of process automation in self-learning factories and product distribution systems with other factories. [9-9]

the Heim Automated Parts Pickup System ( HAPPS). The system automatically translates design parameters and plans from architects, engineers, and clients directly into parametricalgorithmically processed production plans, bills of materials (BOMs) and data needed to operate the fully automated production. Sekisui builds and sells approximately 13,000 Heim-Unit houses annually, including their Zero-Utility Cost House with solar energy generation systems. All the units are prefabricated in the factory to 80% completion, which minimizes signifi cantly the assembly process.[9-9] 

[9-9]
Going back to the fi rst chapter of this section, the robotic technology we fi nd in the car manufacturing industry is still very infl exible, expensive, and needs high levels of expertise to operate. Robotic technology is still in an age very similar to when each computer company or cell phone provider had their own operating system and was not connected to the Internet. However, the robotics technology is about to rapidly accelerate its pace of development.

There are two items that have hindered the explosion of robotics. The fi rst one is a robust operating system across platforms that can propel robot software development; just as iOS and Android did for the explosion of applications in the smartphone platform. Google’s recent acquisition of a large number of robotic companies seems to be geared toward consolidating a universal operating system for robots.

The second issue that has stalled robotics is that the large computation power robots need has been traditionally onboard. This is a largely expensive architecture, that is battery-demanding, cooling-intensive, and creates a space problem. The emerging concept of Cloud robotics will allow robot apparatuses to be connected to the Internet, which permits the migration of their intensive need for computation power to the grid on demand. Robots connected to the Cloud promote collective robot learning from other robots’ experiences and an instantaneous open access to new algorithms—all aspects that will signifi cantly reduce the cost of computing, weight, battery, cooling, and space requirements of robots on the job site.

A robust robotic operating system and an explosive number of applications in the Cloud will signifi cantly lower the cost and expand the design of robotic apparatuses well beyond the fi xed robotic arms we see in manufacturing lines today, eventually transforming the craft-based construction assembly processes and construction equipment that remain relatively unchanged since they consolidated during the industrial revolution.[9-9]

[9-11]
At the Dawn of Three New Manufacturing Eras

3-D manufacturing today encompasses automated additive technologies such as 3-D printing and subtractive technologies like computercontrolled machines ( CNC), laser and water cutters, as well as automated assembly technologies such as industrial robots, quadricopters, and other programmable equipment.

The fi rst thing to understand about computer-controlled 3-D manufacturing and 3-D printing is that these technologies are not going away. On the contrary, they are growing exponentially in many different directions in a very short time frame. What we are witnessing today is just the fi rst generation of digital manufacturing. Computer-controlled manufacturing will be transforming in the coming years in three different distinct stages:

1. 3-D digitally controlled manufacturing: Today we are at the maturing stages of the fi rst era of digital manufacturing in which 3-D printers, CNC, laser cutters, robotic arms, and a whole array of digitally automated machines can print, cut, and carve any shape on industrialized materials.

2. 4-D digitally controlled manufacturing: In a second period sophisticated multimaterial printers and nanotechnology will allow us to create new materials that can be designed and fabricated at a microscopic and atomic level. These new artifi cial materials will perform more effi ciently than raw industrialized materials and will have behaviors that cannot be found in natural materials.

3. n-D digitally controlled manufacturing: In a third period there will be the emergence of programmable matter, synthetic biology, and evolutionary robotics; it will be an epoch in which we can manufacture digitally transformable matter that can be programmed at will. We will also witness the emergence of apparatuses that can self-design and self-manufacture at different scales.

The advent of new multimaterials printers also implies that the designer and the design process will also have to change. Traditional design processes that use CAD or BIM are usually unable to plan for material performance at the macroscopic and microscopic level. Design automation will have to play an increasingly important role in design synthesis for the construction elements that use multimaterials. Jonathan Hiller and Hod Lipson from the Creative Machine Lab at Cornell University have presented a genetic algorithm ( GA) method that is used to optimize the geometry of a multimaterial cantilever beam [2].

These authors state that the GAs are “suitable for designing the complex multi-material objects that have recently become possible to fabricate using additive manufacturing techniques... Instead of designing an object using traditional CAD programs, genetic algorithms allow an engineer to simply set high-level goals to be fulfi lled and the blueprint is autonomously generated” [2].

A second period of digital manufacturing will emerge when technologies such as 4-D multimaterial printers and nanotechnology mature to alter materials at a very small scale. In this second age we will be able to digitally manufacture materials that cannot be found in nature. Further in the future, a fi nal third period of multidimensional or n-D digital manufacturing will emerge as materials can be programmed, bio-engineered, and selfreplicated at even a nanometer scale.[9-11]

## 8.	交互硬件与信息数据流；

## 9.	图表报告及制图

## misc
3. Workflow parametric: A third type of narrative is emerging inside design firms that are using parametric features to automate specific design workflows for projects such as façade design, environmental benchmarking, or structural optimization procedures. These groups are usually project-driven, part of special units inside the fi rms, and they work in aiding designers to explore generative and analytical computational processes in design.
[9-2]

In order to design these types of integrated systems of systems, designers need better tools for managing the information they are working with[9-5]

## algorithms
A series of bespoke algorithms were developed following underlying mathematical principles inspired from the universal order of orbital motion.[9-6]










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

---

[2]Brady Peters, Terri Peters.Computing the Environment: Digital Design Tools for Simulation and Visualisation of Sustainable Architecture[M].Italy:Wiley, April, 2018: page range.

[2-1]Phil Bernstein. Foreword[M]//[2]:VI-IX

[2-2]Brady Peters,Terri Peters. Introduction—computing the environment: design workflows for the simulation of sustainable architecture [M]//[2]:1-13

[2-3]Terri Peters. New dialogues about energy: performance, carbon and climate [M]//[2]:14-27

[2-4]Brady Peters.Parametric environmental design: simulation and generative processes[M]//[2]:28-42

[2-5]Brady Peters. Designing atmospheres: simulating experience[M]//[2]:43-57

[2-6]Terri Peters.Use data: computing life-cycle and real-time visualisation[M]//[2]:58-73

[2-7]Terri Peters. Near future developments: advances in simulation and real-time feedback[M]//[2]:74-93

[2-8]Brady Peters. Designing environments and simulating experience: foster + partners specialist modelling group [M]//[2]:94-105

[2-9]Terri Peters. Designers need feedback: research and practice by kierantimberlake [M]//[2]:118-127

[2-10]Terri Peters.Architecture shapes performance: gxn advances solar modelling and sensing[M]//[2]:128-137

[2-11]Brady Peters. Bespoke tools for a better world: the art of sustainable design at burohappold engineering [M]//[2]:138-149

[2-12]Brady Peters. Big ideas: information driven design[M]//[2]:150-162

[2-13]Terri Peters. Simulating the invisible: max fordham designs light, air and sound[M]//[2]:162-175

[2-14]Terri Peters. White architects: build the future[M]//[2]:176-183

[2-15]Terri Peters. Core: integrated computation and research[M]//[2]:184-191

[2-16]Brady Peters. Superspace: computing human-centric architecture [M]//[2]:192-200

[2-17]Terri Peters. Zhacode: sketching with performance[M]//[2]:201-209

[2-18]Brady Peters, Terri Peters. Global environmental challenges[M]//[2]:218-235

---

[3]Wassim Jabi. Parametric design for architecture[M]. London:Laurence King Publishing, September, 2013 : page range.

[4]Robert Woodbury. Elements of Parametric Design[M]. New York:Routledge, July, 2010 : page r-ange.

[5]Christopher Beorkrem. Material strategies in digital fabrication[M].Oxon :Routledg, July, 2017:page range.

[6]Carlos BAÑÓN, Félix RASPALL. 3d printing architecture: workflows, applications, and trends [M]. Singapore:Springer, October, 2020:page range.

[7]郭湧.论风景园林信息模型的概念内涵和技术应用体系[J].中国园林,2020,36(09):17-22.

[8]赖文波,杜春兰,贾铠针,江虹.景观信息模型(LIM)框架构建研究——以重庆大学B校区三角地改造为例[J].中国园林,2015,31(07):26-30.

---

[9] Alfredo Andia, Thomas Spiegelhalter.  Post-parametric Automation in Design and Construction[M].Norwood :Artech House, November, 2014

[9-1]Alfredo Andia, Thomas Spiegelhalter. Post-Parametric Automation in Design and Construction[M]//[9]:13-14

[9-2]Alfredo Andia, Thomas Spiegelhalter. Toward Automating Design and Construction[M]//[9]:19-25

[9-3]Alfredo Andia,Thomas Spiegelhalter.Green Automation: Design Optimization, Manufacturing, and Life-Cycle Sustainability[M]//[9]:27-32

[9-4]Alfredo Andia and Thomas Spiegelhalter.Post-Parametric Workflows in Architectural and Engineering Offices[M]//[9]:35-38

[9-5]Keith Besserud.Engaging with Complexity: Computational Algorithms in Architecture and Urban Design[M]//[9]:39-45

[9-6]Abdulmajid Karanouh.Algorithmic Principles for Façade and Building Automation Systems: Al-Bahar Towers, Abu Dhabi[M]//[9]:59-74

[9-7]Clayton Binkley, Paul Jeffries,  Mathew Vola.Design Computation at Arup[M]//[9]:112-118

[9-8]Lars Junghans.Generic Optimization Algorithms for Building Energy Demand Optimization: Concept 2226, Austria[M]//[9]:121-129

[9-9]Alfredo Andia,Thomas Spiegelhalter.Post-Parametric Automation in Construction[M]//[9]:141-144

[9-10]Alfredo Andia.Automating Design via Machine Learning Algorithms[M]//[9]:191-199

[9-11]Alfredo Andia. Automating Construction via n-D Digital Manufacturing[M]//[9]:201-206

---

[10]Benjamin Aranda.Tooling[M].New York:Princeton Architectural Pres, December, 2005.

---

[11] Christoph Gengnagel,Christoph Gengnagel,Jane Burry editor.Impact: Design With All Senses: Proceedings of the Design Modelling Symposium, Berlin 2019[M].Switzerland:Springer,August, 2019

[11-1]Zeynep Aksöz,Clemens Preisinger.An Interactive Structural Optimization of Space Frame Structures Using Machine Learning[M]//[11]:18-31
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE2NzAyNDcyNTMsLTQ1NDI5ODAyOSw3Nj
gyMjc4NCwtNDkzMjA4MTU4LDY4MDY2MTIzLC0yMDA4MjgzODY0
LC0xNTc0NTU3MDI0LC0xMTQyNjM2Njk1LDc3ODIwODE1OSwtMz
YyNjg1OTc5LDIwMzY2MzAzMDgsMTEzOTY3MTgwOSwxOTMxMTcw
MDAwLDE1MTcwODc3MzMsMTg4ODI0MDEsLTE1ODQyMTc2MTMsLT
EwNjQ2ODA0NDQsLTkyNTQ0MjA0NiwtMTkyODA5MTc1MSwxNTk0
NjczOTM5XX0=
-->