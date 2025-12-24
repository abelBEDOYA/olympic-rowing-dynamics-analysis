// Site configuration - Edit this file to customize your personal info and links

export const siteConfig = {
    // Personal information for the landing page
    author: {
        name: "Abel Bedoya",
        role: "Researcher & Developer",
        github: "https://github.com/abelBEDOYA",
        linkedin: "https://www.linkedin.com/in/abel-gonzalez-bernad/",
        email: "abelgonzalezbernad@gmail.com",
    },

    // Project info
    project: {
        name: "Olympic Rowing Dynamics",
        repository: "https://github.com/abelBEDOYA/olympic-rowing-dynamics-analysis",
    },

    // Hero section background image (place your image in /public/img/)
    heroImage: "/img/background.jpg",

    // Documentation files (place PDFs in /public/docs/)
    docs: [
        {
            title: "Technical Documentation",
            description: "Mathematical foundations of the rower-boat-water system",
            file: "/docs/polinomical_solution_air_phase.pdf",
        },
    ],
};

export default siteConfig;
