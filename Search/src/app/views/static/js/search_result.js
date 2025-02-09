// Sample book data
const books = [
    {
        title: 'Book Title 1',
        author: 'Author Name 1',
        isbn: '978-1234567890',
        cover: 'var(--book-cover-1)'
    },
    {
        title: 'Book Title 2',
        author: 'Author Name 2',
        isbn: '978-2345678901',
        cover: 'var(--book-cover-2)'
    },
    {
        title: 'Book Title 3',
        author: 'Author Name 3',
        isbn: '978-3456789012',
        cover: 'var(--book-cover-3)'
    },
    {
        title: 'Book Title 4',
        author: 'Author Name 4',
        isbn: '978-4567890123',
        cover: 'var(--book-cover-4)'
    },
    {
        title: 'Book Title 5',
        author: 'Author Name 5',
        isbn: '978-5678901234',
        cover: 'var(--book-cover-1)'
    },
    {
        title: 'Book Title 6',
        author: 'Author Name 6',
        isbn: '978-6789012345',
        cover: 'var(--book-cover-2)'
    }
];

// Function to create book cards
function createBookCard(book) {
    const card = document.createElement('div');
    card.className = 'book-card';
    
    card.innerHTML = `
        <div class="book-cover" style="background-color: ${book.cover}"></div>
        <div class="book-info">
            <p><strong>TITLE:</strong> ${book.title}</p>
            <p><strong>AUTHOR:</strong> ${book.author}</p>
            <p><strong>ISBN:</strong> ${book.isbn}</p>
        </div>
    `;
    
    return card;
}

// Function to render books
function renderBooks(booksArray) {
    const booksGrid = document.getElementById('booksGrid');
    booksGrid.innerHTML = '';
    
    booksArray.forEach(book => {
        booksGrid.appendChild(createBookCard(book));
    });
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    renderBooks(books);
    
    // Add event listeners for filters
    document.querySelectorAll('input[name="genre"], input[name="rating"]').forEach(input => {
        input.addEventListener('change', (e) => {
            // In a real application, you would filter the books based on the selected options
            // For this demo, we'll just re-render the same books
            renderBooks(books);
        });
    });
});