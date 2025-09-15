// Main JavaScript for Araiza Inc Website

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initNavigation();
    initAnimations();
    initFormValidation();
    initTooltips();
    initDropdowns();
    
});

// Navigation functionality
function initNavigation() {
    // Handle dropdown submenus
    const dropdownSubmenus = document.querySelectorAll('.dropdown-submenu');
    
    dropdownSubmenus.forEach(function(submenu) {
        submenu.addEventListener('mouseenter', function() {
            const submenuDropdown = this.querySelector('.dropdown-menu');
            if (submenuDropdown) {
                submenuDropdown.classList.add('show');
            }
        });
        
        submenu.addEventListener('mouseleave', function() {
            const submenuDropdown = this.querySelector('.dropdown-menu');
            if (submenuDropdown) {
                submenuDropdown.classList.remove('show');
            }
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add active class to current page nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        }
    });
}

// Animation functionality
function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards and sections
    const animatedElements = document.querySelectorAll('.card, .hero-section > div');
    animatedElements.forEach(function(element) {
        observer.observe(element);
    });

    // Counter animation for stats
    const counters = document.querySelectorAll('.counter');
    counters.forEach(function(counter) {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60fps
        let current = 0;

        const updateCounter = function() {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };

        // Start counter when element is visible
        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    updateCounter();
                    counterObserver.unobserve(entry.target);
                }
            });
        });

        counterObserver.observe(counter);
    });
}

// Form validation functionality
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            let firstInvalidField = null;

            // Remove previous error states
            form.querySelectorAll('.is-invalid').forEach(function(field) {
                field.classList.remove('is-invalid');
            });

            // Validate required fields
            requiredFields.forEach(function(field) {
                const value = field.value.trim();
                
                if (!value) {
                    field.classList.add('is-invalid');
                    isValid = false;
                    if (!firstInvalidField) {
                        firstInvalidField = field;
                    }
                } else if (field.type === 'email' && !isValidEmail(value)) {
                    field.classList.add('is-invalid');
                    isValid = false;
                    if (!firstInvalidField) {
                        firstInvalidField = field;
                    }
                }
            });

            if (!isValid) {
                e.preventDefault();
                if (firstInvalidField) {
                    firstInvalidField.focus();
                    showNotification('Por favor complete todos los campos requeridos correctamente.', 'error');
                }
            } else {
                // Show loading state for submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';
                    
                    // Reset button after 5 seconds (in case of redirect failure)
                    setTimeout(function() {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalText;
                    }, 5000);
                }
            }
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(function(input) {
            input.addEventListener('blur', function() {
                validateField(this);
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

// Validate individual field
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;

    // Remove previous error state
    field.classList.remove('is-invalid');

    // Check if required field is empty
    if (field.hasAttribute('required') && !value) {
        isValid = false;
    }

    // Email validation
    if (field.type === 'email' && value && !isValidEmail(value)) {
        isValid = false;
    }

    // Phone validation (basic)
    if (field.type === 'tel' && value && !isValidPhone(value)) {
        isValid = false;
    }

    if (!isValid) {
        field.classList.add('is-invalid');
    }

    return isValid;
}

// Email validation helper
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Phone validation helper
function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[0-9\s\-\(\)]{8,}$/;
    return phoneRegex.test(phone);
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize dropdowns
function initDropdowns() {
    // Category/Service dropdown functionality
    const categoriaSelect = document.getElementById('categoria_id');
    const servicioSelect = document.getElementById('servicio_id');
    
    if (categoriaSelect && servicioSelect) {
        categoriaSelect.addEventListener('change', function() {
            const categoriaId = this.value;
            
            // Reset service select
            servicioSelect.innerHTML = '<option value="">Cargando servicios...</option>';
            servicioSelect.disabled = true;
            
            if (categoriaId) {
                // Fetch services for the selected category
                fetch(`/api/servicios/${categoriaId}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        servicioSelect.innerHTML = '<option value="">Selecciona un servicio (opcional)</option>';
                        
                        data.forEach(service => {
                            const option = document.createElement('option');
                            option.value = service.id;
                            option.textContent = service.nombre;
                            servicioSelect.appendChild(option);
                        });
                        
                        servicioSelect.disabled = false;
                    })
                    .catch(error => {
                        console.error('Error loading services:', error);
                        servicioSelect.innerHTML = '<option value="">Error cargando servicios</option>';
                        showNotification('Error al cargar los servicios. Por favor intente de nuevo.', 'error');
                    });
            } else {
                servicioSelect.innerHTML = '<option value="">Primero selecciona una categoría</option>';
                servicioSelect.disabled = true;
            }
        });
    }
}

// Notification system
function showNotification(message, type = 'info', duration = 5000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(function() {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

// Image lazy loading
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.removeAttribute('data-src');
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(function(img) {
        imageObserver.observe(img);
    });
}

// Search functionality (if needed)
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            clearTimeout(searchTimeout);
            
            if (query.length >= 3) {
                searchTimeout = setTimeout(function() {
                    performSearch(query);
                }, 300);
            } else {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
            }
        });
    }
}

// Perform search (placeholder function)
function performSearch(query) {
    // This would typically make an AJAX request to a search endpoint
    console.log('Searching for:', query);
    // Implement actual search functionality here
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = function() {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Handle form submissions with AJAX (optional enhancement)
function handleAjaxForms() {
    const ajaxForms = document.querySelectorAll('.ajax-form');
    
    ajaxForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';
            
            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    form.reset();
                } else {
                    showNotification(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Hubo un error al enviar el formulario. Por favor intente de nuevo.', 'error');
            })
            .finally(() => {
                // Reset button
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            });
        });
    });
}

// Export functions for global use
window.AraizaInc = {
    showNotification,
    validateField,
    isValidEmail,
    isValidPhone,
    debounce,
    throttle
};