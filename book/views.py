from django.shortcuts import render, get_object_or_404, redirect
from . models import Book
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def issue_book(request):
    books = Book.objects.all().order_by('-issue_date')
    book = Book.objects.filter(is_returned = False)
    return render(request, 'book/issue_book.html', {'books': books, 'book': book})

def create_issue_book(request):
    if request.method == 'POST':
        image_book = request.FILES.get('image_book')
        name = request.POST.get('name')
        author = request.POST.get('author')
        borrower_name = request.POST.get('borrower_name')
        
        Book.objects.create(
            user = request.user,
            image_book = image_book,
            name = name,
            author = author,
            borrower_name = borrower_name
        )
        messages.success(request, 'The Creation of issue book is successful.')
        return redirect('issue_book')
    return render(request, 'book/create_issue_book.html')

def edit_issue_book(request, pk):
    books = get_object_or_404( Book, id = pk )
    
    if request.method == 'POST':
        name = request.POST.get('name')
        image_book = request.FILES.get('image_book')
        author = request.POST.get('author')
        borrower_name = request.POST.get('borrower_name')

        books.user = request.user
        books.name = name
        books.author = author
        books.borrower_name = borrower_name
        if image_book:
            books.image_book = image_book
        books.save()
        messages.success(request, 'The edit of book is successful.')
        return redirect('issue_book')
    return render(request, 'book/edit_issue_book.html', {'books': books})

def detail_issue_book(request, pk):
    books = get_object_or_404( Book, id = pk )
    return render(request, 'book/detail_issue_book.html', {'books': books})

def delete_issue_book(request, pk):
    book = get_object_or_404( Book, id = pk, user = request.user )
    book.delete()
    messages.success( request, 'The book is deleted.')
    return redirect('home')

def update_issue_book(request, pk):
    books = Book.objects.get( id = pk )
    if books:
        books.is_returned = True
        books.save()
        messages.success(request, 'The book is returend.')
        return redirect('detail_issue_book', pk = pk)
    
def search(request):
    query = request.GET.get('search', '') or ''
    query = query.strip()
    books = Book.objects.none()
    if query:
        books = Book.objects.filter(
            Q(name__icontains=query)
            | Q(author__icontains=query)
            | Q(borrower_name__icontains=query)
        )
    return render(request, 'book/search.html', {'query': query, 'books': books })