from django.shortcuts import (
    render, redirect
)
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import (
    DetailView,ListView
)
from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger
)
from .models import (
    Product, ProductImage, Quotation
)
from customer.models import (
    Review, 
)
from .forms import (
    QuotationForm, QuotationTrackingForm
)
import random
random.seed(1)

class Node:
    def __init__(self, key):
        self.val = key
        self.right = None

def createRightSkewedTree(hasUpdates,nextReviews,reveiews):
    if hasUpdates:
        treeList = []
        for review in nextReviews:
            tree = Node(review)
            repliedReviews = reveiews.filter(previous_review_id = review.review_id)
            tree.right = createRightSkewedTree(len(repliedReviews)!=0, repliedReviews, reveiews)
            treeList.append(tree)
        return treeList
    return None

def get_anonymous_user():
    return get_user_model().objects.get_or_create(username='anonymous.user')[0]

                 
class About(View):

    def get(self, request, *args, **kwargs):
        return render(request,'mainapp/aboutus.html')

class GalleryView(View):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        productImages = ProductImage.objects.all()
        productsForGallery = [[product.product_id, product.image.url] for product in products] + [[product.product_id, product.img_file.url] for product in productImages]
        

        requested_page = request.GET.get('page', 1)
        paginator = Paginator(productsForGallery, 10)
        
        try:
            data = paginator.page(requested_page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        image_list = data.object_list
        random.shuffle(image_list)
        data.object_list = image_list
        
        return render(request,'mainapp/gallery.html', {'data':data})
    
class Index(View):

    def get(self, request, *args, **kwargs):
        product_list = Product.objects.all()
        requested_page = request.GET.get('page', 1)
        paginator = Paginator(product_list, 4)
        
        try:
            products = paginator.page(requested_page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
            
        return render(request, "mainapp/index.html", {'products':products})

class ProductDetailView(DetailView):

    model = Product
    template_name = "mainapp/productDetail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        product = super().get_context_data(**kwargs)       
        ProductImagesToThisProduct = ProductImage.objects.filter(product_id = product['product'].product_id)
        product['has_product_images'] = len(ProductImagesToThisProduct)>0
        product['productImages'] = ProductImagesToThisProduct

        reviews = Review.objects.all()
        reviewsForProduct = reviews.filter(product_id=product['product'].product_id).order_by('update_date')
        hasReviews = len(reviewsForProduct) != 0
        product['hasReviews'] = int(hasReviews)
        rightSkewedTreeList = ''
        
        if hasReviews:
            treeList = createRightSkewedTree(hasReviews, reviewsForProduct, reviews)
            
            
            rightSkewedTreeList = treeList
        product['rightSkewedTreeList']=rightSkewedTreeList
        productContextForCustomerReviewMacro = {'pcfcrm': {'product_id':product['product'].product_id,
                                                           'hasReviews':int(hasReviews),
                                                           'rightSkewedTreeList':rightSkewedTreeList
                                                           }
                                                }
        product['productContextForCustomerReviewMacro']=productContextForCustomerReviewMacro
        return product

class ProductView(ListView):
    model = Product
    template_name = "mainapp/product_list.html"
    context_object_name = 'products'  
    paginate_by = 3    

    def get_queryset(self):
        queryset = Product.objects.all()
        productImages = ProductImage.objects.all()
        productwithImages = []
        for prod in queryset:
            prodDict = dict(prod.__dict__)
            ProductImagesToThisProduct = productImages.filter(product_id = prod.product_id)
            prodDict['has_product_images'] = len(ProductImagesToThisProduct)>0
            prodDict['productImages'] = ProductImagesToThisProduct
            
            reviews = Review.objects.all()
            reviewsForProduct = reviews.filter(product_id=prod.product_id).order_by('update_date')
            hasReviews = len(reviewsForProduct) != 0
            prodDict['hasReviews'] = int(hasReviews)
            rightSkewedTreeList = ''
            
            if hasReviews:
                treeList = createRightSkewedTree(hasReviews, reviewsForProduct, reviews)
                
                
                rightSkewedTreeList = treeList
            prodDict['rightSkewedTreeList']=rightSkewedTreeList
            productwithImages.append(prodDict)

        return productwithImages

class QuotationView(View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id', 0)
        product = Product.objects.filter(product_id = product_id)[0]
        product = product
        quotation = f'''
Product Name: {product.product_name}
Product Description: {product.desc}
Product Price: {product.price}
If you want to buy this product enter you details in this form
and we will be get in touch with you in next 2 working days via phone or email
to confirm your order.

Note:
The aproximate time to deliver the product is 10-15 days from order placed.
The delivery charges on the product may vary from place and weight of the product.
                    '''
        customization = "If you want to add or get something remove or if you have any other query related to this product. Please write to us."
        
        if request.user.is_authenticated:
            user = request.user
            first_name = user.first_name
            last_name = user.last_name
            email = user.email
            initialform_data = {
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'product':product,
                'quotation':quotation,
                'customization':customization
                }
            
            form = QuotationForm(initialform_data)
            return render(request, "mainapp/addquotaion.html", {'form':form, 'product':product})
        else:
            initialform_data = {                
                'product':product,
                'quotation':quotation,
                'customization':customization
                }
            form = QuotationForm(initialform_data)
            return render(request, "mainapp/addquotaion.html", {'form':form, 'product':product})

    def post(self, request, *args, **kwargs):
        
        product_id = kwargs.get('product_id', 0)
        product = Product.objects.filter(product_id = product_id)[0]
        quotation_text = f'''
Product Name: {product.product_name}
Product Description: {product.desc}
Product Price: {product.price}
If you want to buy this product enter you details in this form
and we will be get in touch with you in next 2 working days via phone or email
to confirm your order.

Note:
The aproximate time to deliver the product is 10-15 days from order placed.
The delivery charges on the product may vary from place and weight of the product.
                    '''
        initialform_data = {
                'product':product,
                'quotation':quotation_text
                }
        form = QuotationForm(request.POST, initial = initialform_data)
        
        if form.is_valid():
            
            quotation = form.save(commit=False)
            quotation.product = product
            quotation.quotation = quotation_text
            
            if request.user.is_authenticated:
                user = request.user
            else:
                user = get_anonymous_user()
            quotation.user = user
            quotation.save()
            successMessage = f"We have successfully create a quotation for you. you can use the quotation id: {quotation.quotation_id} or your email to track the status of your quotation."
            messages.success(request,successMessage)
            return redirect('querysuccess')    
        
        return render(request, "mainapp/addquotaion.html", {'form': form, 'product':product})

class QuotationTrackingView(View):

    def get(self, request, *args, **kwargs):
        form=QuotationTrackingForm()
        return render(request, "mainapp/quotationtrackingform.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = QuotationTrackingForm(request.POST)
        
        if form.is_valid():
            tracking_id = form.cleaned_data.get('tracking_id')
            email = form.cleaned_data.get('email')
            initial_data = {'tracking_id':tracking_id,
                            'email':email
                            }
            quotation = Quotation.objects.all()
            resultantQuotation = {"hasQuotation":0}
            if tracking_id and email:                
                quotationThroughEmail = quotation.filter(email=email)
                if len(quotationThroughEmail)>0:
                    quotationThroughTrackingId = quotationThroughEmail.filter(quotation_id=tracking_id)
                    if len(quotationThroughTrackingId)==1:
                        resultantQuotation["hasQuotation"] = 1
                        resultantQuotation["quotations"] = quotationThroughTrackingId
                    else:
                        resultantQuotation["message"] = "No record found for the given Tracking Id. Please enter the correct Id which you received during the Quote submission or enter your Email you used during quote submission to get the details on your quotations."
                else:
                    resultantQuotation["message"] = "No record found for the given Email Id. Please enter the correct Tracking Id which you received during the Quote submission or enter your Email you used during quote submission to get the details on your quotations."
            elif tracking_id:
                quotationThroughTrackingId = quotation.filter(quotation_id=tracking_id)
                if len(quotationThroughTrackingId)==1:
                    resultantQuotation["hasQuotation"] = 1
                    resultantQuotation["quotations"] = quotationThroughTrackingId
                else:
                    resultantQuotation["message"] = "No record found for the given Tracking Id. Please enter the correct Id which you received during the Quote submission or enter your Email you used during quote submission to get the details on your quotations."
            elif email:
                quotationThroughEmail = quotation.filter(email=email)
                if len(quotationThroughEmail)>0:
                    resultantQuotation["hasQuotation"] = 1
                    resultantQuotation["quotations"] = quotationThroughEmail
                else:
                    resultantQuotation["message"] = "No record found for the given Email Id. Please enter the correct Tracking Id which you received during the Quote submission or enter your Email you used during quote submission to get the details on your quotations."
            else:
                resultantQuotation["message"] = "Please enter either Tracking Id or Email or both."
            form=QuotationTrackingForm(initial_data)
            return render(request,
                          "mainapp/quotationtrackingform.html",
                          {
                              'form': form,
                              'resultantQuotation':resultantQuotation
                              }
                          )
        else:
            
            return render(request, "mainapp/quotationtrackingform.html", {'form': form})
