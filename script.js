document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    lucide.createIcons();

    // 1. Theme Toggle Logic
    const themeToggleBtn = document.getElementById('theme-toggle');
    const body = document.body;

    // Check saved theme or system preference
    const savedTheme = localStorage.getItem('theme') || 'dark-mode';
    body.className = savedTheme;

    themeToggleBtn.addEventListener('click', () => {
        if (body.classList.contains('dark-mode')) {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            localStorage.setItem('theme', 'light-mode');
        } else {
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        }
    });

    // 2. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navMenu = document.getElementById('nav-menu-id');
    const menuIcon = mobileMenuBtn.querySelector('.menu-icon');
    const closeIcon = mobileMenuBtn.querySelector('.close-icon');

    mobileMenuBtn.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        menuIcon.classList.toggle('hidden');
        closeIcon.classList.toggle('hidden');
    });

    // Close mobile menu when a nav link is clicked
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            menuIcon.classList.remove('hidden');
            closeIcon.classList.add('hidden');
        });
    });

    // 3. Header scroll class & active navigation link on scroll
    const header = document.getElementById('main-header');
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section');

    window.addEventListener('scroll', () => {
        // Scroll header effect
        if (window.scrollY > 50) {
            header.style.padding = '10px 0';
            header.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.padding = '0';
            header.style.boxShadow = 'none';
        }

        // Active link tracking
        let currentSectionId = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 120;
            const sectionHeight = section.clientHeight;
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                currentSectionId = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === currentSectionId) {
                link.classList.add('active');
            }
        });
    });

    // 4. Custom Typing Effect
    const typedTextSpan = document.getElementById('typed-text');
    const roles = ["Data Analyst", "AI/ML Enthusiast", "Power BI Developer", "Python Developer"];
    const typingDelay = 100;
    const erasingDelay = 60;
    const newRoleDelay = 2000;
    let roleIndex = 0;
    let charIndex = 0;

    function type() {
        if (charIndex < roles[roleIndex].length) {
            typedTextSpan.textContent += roles[roleIndex].charAt(charIndex);
            charIndex++;
            setTimeout(type, typingDelay);
        } else {
            setTimeout(erase, newRoleDelay);
        }
    }

    function erase() {
        if (charIndex > 0) {
            typedTextSpan.textContent = roles[roleIndex].substring(0, charIndex - 1);
            charIndex--;
            setTimeout(erase, erasingDelay);
        } else {
            roleIndex++;
            if (roleIndex >= roles.length) roleIndex = 0;
            setTimeout(type, typingDelay + 300);
        }
    }

    if (typedTextSpan) {
        setTimeout(type, 1000);
    }

    // 5. Scroll Reveal Animations (Intersection Observer)
    const revealElements = document.querySelectorAll('.scroll-reveal');
    const revealOnScroll = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => revealOnScroll.observe(el));

    // Project Filtering Logic
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            projectCards.forEach(card => {
                const category = card.getAttribute('data-category');
                if (filterValue === 'all' || category === filterValue) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });

    // 6. Interactive Resume Chatbot Widget Logic
    const chatbotWidget = document.getElementById('chatbot-widget-id');
    const chatbotToggleBtn = document.getElementById('chatbot-toggle-btn-id');
    const chatbotWindow = document.getElementById('chatbot-window-id');
    const chatOpenIcon = chatbotToggleBtn.querySelector('.chat-open-icon');
    const chatCloseIcon = chatbotToggleBtn.querySelector('.chat-close-icon');
    const chatbotForm = document.getElementById('chatbot-form-id');
    const chatbotInput = document.getElementById('chatbot-input-id');
    const chatbotMessages = document.getElementById('chatbot-messages-id');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');

    // Open/Close Chatbot Window
    chatbotToggleBtn.addEventListener('click', () => {
        chatbotWindow.classList.toggle('hidden');
        chatOpenIcon.classList.toggle('hidden');
        chatCloseIcon.classList.toggle('hidden');
        const pulse = chatbotToggleBtn.querySelector('.chat-pulse');
        if(pulse) pulse.classList.toggle('hidden');
        
        // Scroll to bottom when opening
        if (!chatbotWindow.classList.contains('hidden')) {
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
            chatbotInput.focus();
        }
    });

    // Chatbot Knowledge Base
    const resumeData = {
        skills: {
            keywords: ['skill', 'skills', 'know', 'tech', 'stack', 'languages', 'programming', 'tools', 'power bi', 'tableau', 'excel'],
            response: "Sangram's core skills include:<br>" +
                      "• <strong>Data Analytics & Visualization:</strong> Power BI, Tableau, Excel & Advanced Excel, EDA, Statistics, Matplotlib, Seaborn.<br>" +
                      "• <strong>ML & AI:</strong> Scikit-learn, XGBoost, TensorFlow, PyTorch, OpenCV, LangChain, LangGraph, RAG Pipelines, LLM APIs, Vector Databases, Time Series.<br>" +
                      "• <strong>Programming:</strong> Python, SQL (MySQL, PostgreSQL), R, JavaScript, C++, DSA, OOP, System Design.<br>" +
                      "• <strong>Data Engineering & Tools:</strong> ETL Pipelines, FastAPI, Streamlit, Docker, MongoDB, AWS, Django, Flask, n8n, Zapier."
        },
        experience: {
            keywords: ['experience', 'work', 'intern', 'internship', 'company', 'variant', 'sumago', 'job'],
            response: "Sangram has completed two valuable internships:<br><br>" +
                      "1. <strong>Data Science Intern @ AI Variant</strong> (Remote, July 2025 – April 2026): Performed EDA on 500K+ row datasets, built Power BI KPI dashboards, automated ETL pipelines in Python & SQL, deployed Time Series Forecasting models, and developed autonomous AI agents on AWS.<br><br>" +
                      "2. <strong>Data Science Intern @ Sumago Infotech</strong> (Onsite, Dec 2024 – Feb 2025): Constructed regression-based predictive models with complete data preprocessing, feature engineering, and performance evaluations."
        },
        projects: {
            keywords: ['project', 'projects', 'build', 'built', 'sales', 'segmentation', 'churn', 'forecasting', 'reporting', 'hr', 'attrition', 'rag', 'erp', 'automation', 'anomaly'],
            response: "Sangram has built high-impact projects in both AI/ML and Data Analytics:<br><br>" +
                      "<strong>AI & Machine Learning:</strong><br>" +
                      "• <strong>RAG Document Intelligence:</strong> Hybrid search with 87% answer relevance. Deployed via FastAPI & Docker.<br>" +
                      "• <strong>Intelligent Workflow Automation:</strong> API-driven agentic pipelines saving 20+ hrs/month, with LLM structured outputs.<br>" +
                      "• <strong>Real-Time Predictive Analytics:</strong> XGBoost & LSTM models detecting anomalies on live event streams with Kafka.<br>" +
                      "• <strong>AI-Powered ERP:</strong> Facial attendance integration using face-api.js and ESP32 IoT.<br><br>" +
                      "<strong>Data Analytics & BI:</strong><br>" +
                      "• <strong>Real-Time Sales Dashboard:</strong> End-to-end pipeline with interactive Power BI & Streamlit dashboard, reducing reporting time by 40%.<br>" +
                      "• <strong>Customer Segmentation & Churn:</strong> K-Means clustering and churn models on 200K+ customer records.<br>" +
                      "• <strong>Demand Forecasting Pipeline:</strong> ETL pipeline with ARIMA & XGBoost for time-series forecasting and structured Excel reports.<br>" +
                      "• <strong>HR Attrition Analytics:</strong> Statistical hypothesis testing and Tableau dashboard, reducing reporting effort by 30%."
        },
        education: {
            keywords: ['education', 'college', 'degree', 'study', 'cgpa', 'school', 'marks', 'percentage', 'hsc', 'ssc'],
            response: "Sangram's educational details are:<br>" +
                      "• <strong>B.E. in Artificial Intelligence & Machine Learning</strong> from Samarth College of Engineering & Management, Belhe, Pune (CGPA: <strong>8.64</strong>, Graduating June 2026).<br>" +
                      "• <strong>HSC</strong> from Dada Patil Mahavidyalaya, Karjat (Percentage: <strong>65%</strong>, 2022).<br>" +
                      "• <strong>SSC</strong> from Mahatma Gandhi Vidyalaya, Karjat (Percentage: <strong>88%</strong>, 2020)."
        },
        contact: {
            keywords: ['contact', 'email', 'phone', 'number', 'address', 'location', 'reach', 'hire', 'github', 'linkedin'],
            response: "You can reach out to Sangram through:<br>" +
                      "• <strong>LinkedIn:</strong> <a href='https://www.linkedin.com/in/sangram-deshmukh-530b512aa' target='_blank'>linkedin.com/in/sangram-deshmukh-530b512aa</a><br>" +
                      "• <strong>Email:</strong> <a href='mailto:sangramdeshmukh2004@gmail.com'>sangramdeshmukh2004@gmail.com</a><br>" +
                      "• <strong>Phone:</strong> <a href='tel:+919270836897'>+91 9270836897</a> / <a href='tel:+919561563002'>+91 9561563002</a><br>" +
                      "• <strong>Location:</strong> Pune, India<br>" +
                      "• <strong>GitHub:</strong> <a href='https://www.github.com/sangram654' target='_blank'>github.com/sangram654</a>"
        },
        awards: {
            keywords: ['award', 'awards', 'achievement', 'achievements', 'topper', 'prize', 'competition', 'certifications', 'certification'],
            response: "Sangram has earned several notable recognitions:<br>" +
                      "• <strong>Academic Topper:</strong> Ranked #1 topper student in the AI & ML Dept (Academic Year 2024-25).<br>" +
                      "• <strong>1st Prize:</strong> Won inter-campus General Knowledge Competition.<br>" +
                      "• <strong>Certifications:</strong> Udemy Power BI Data Analysis, Flipkart Grid 6.0 Tech Quiz Hackathon participant."
        },
        hobbies: {
            keywords: ['hobby', 'hobbies', 'chess', 'music', 'interest', 'interests'],
            response: "Sangram's hobbies include:<br>" +
                      "• <strong>Chess:</strong> Enjoy playing chess as a leisure activity; it helps him unwind while keeping his mind sharp and focused.<br>" +
                      "• <strong>Music:</strong> Listening to music across various genres to relax and recharge during breaks."
        },
        about: {
            keywords: ['about', 'who are you', 'hello', 'hi', 'hey', 'summary'],
            response: "Sangram Deshmukh is an entry-level Data Analyst and AI/ML Enthusiast. He has expertise in data analysis, BI tools (Power BI, Tableau), predictive modelling, and custom data workflows. He is based in Pune, India, and is open for role opportunities!"
        }
    };

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;
        msgDiv.innerHTML = text;
        chatbotMessages.appendChild(msgDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    async function handleUserInput(input) {
        const query = input.toLowerCase().trim();
        if (!query) return;

        appendMessage('user', input);
        chatbotInput.value = '';

        // Typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message bot-message typing-indicator';
        typingIndicator.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
        chatbotMessages.appendChild(typingIndicator);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

        // CSS inline adjustments for typing indicator spacing
        typingIndicator.style.display = 'flex';
        typingIndicator.style.gap = '4px';
        typingIndicator.style.alignItems = 'center';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: input })
            });

            if (!response.ok) {
                throw new Error("API responded with an error status.");
            }

            const result = await response.json();
            if (result.status === 'success') {
                typingIndicator.remove();
                appendMessage('bot', result.reply);
                return;
            } else {
                throw new Error(result.reply || "API response status was not successful.");
            }
        } catch (err) {
            console.warn("Real-time chatbot API failed, falling back to local static brain:", err);
        }

        // Local Fallback Keyword Brain Logic
        let foundResponse = null;
        for (const category in resumeData) {
            const data = resumeData[category];
            const isMatch = data.keywords.some(kw => query.includes(kw));
            if (isMatch) {
                foundResponse = data.response;
                break;
            }
        }

        if (!foundResponse) {
            foundResponse = "I couldn't quite find details matching that query. You can ask me about:<br>" +
                            "• His <strong>skills</strong> (Power BI, SQL, Python, Tableau)<br>" +
                            "• His professional <strong>experience</strong><br>" +
                            "• His analytics <strong>projects</strong> (Sales Dashboard, HR Analytics)<br>" +
                            "• His <strong>education</strong> details<br>" +
                            "• How to <strong>contact</strong> him or view his LinkedIn";
        }

        // Simulate a slight thinking delay for local fallback
        setTimeout(() => {
            typingIndicator.remove();
            appendMessage('bot', foundResponse);
        }, 500);
    }

    chatbotForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handleUserInput(chatbotInput.value);
    });

    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            handleUserInput(btn.textContent);
        });
    });

    // 7. Contact Form Handling
    const contactForm = document.getElementById('contact-form');
    const formStatus = document.getElementById('form-status');

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('.form-btn');
            const originalText = submitBtn.innerHTML;
            
            // Get form values
            const name = document.getElementById('form-name').value;
            const email = document.getElementById('form-email').value;
            const subject = document.getElementById('form-subject').value;
            const message = document.getElementById('form-message').value;

            // Visual loading feedback
            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Sending... <span class="pulse-dot"></span>';
            
            try {
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name, email, subject, message })
                });

                const result = await response.json();

                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;

                if (response.ok && result.status === 'success') {
                    // Show success status
                    formStatus.textContent = "Thank you! Your message has been sent successfully. Sangram will get back to you shortly.";
                    formStatus.className = "form-status success";
                    formStatus.classList.remove('hidden');
                    contactForm.reset();
                } else {
                    throw new Error(result.detail || 'Failed to submit form.');
                }
            } catch (err) {
                console.error("Submission error:", err);
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
                
                // Show error status
                formStatus.textContent = "Oops! Something went wrong. Please check your inputs and try again.";
                formStatus.className = "form-status error";
                formStatus.classList.remove('hidden');
            }

            // Hide status after 6 seconds
            setTimeout(() => {
                formStatus.classList.add('hidden');
            }, 6000);
        });
    }
});
