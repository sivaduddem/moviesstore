from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Movie, Review, ReviewReply


class ReviewReplyTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='tester', password='pass')
		# Use a simple image path; tests do not load the file
		self.movie = Movie.objects.create(name='Test Movie', price=10, description='Desc', image='movie_images/avatar.jpg')

	def test_create_reply(self):
		# create a review
		self.client.login(username='tester', password='pass')
		create_review_url = reverse('movies.create_review', args=[self.movie.id])
		response = self.client.post(create_review_url, {'comment': 'Great!'})
		self.assertEqual(response.status_code, 302)
		review = Review.objects.filter(movie=self.movie).first()
		self.assertIsNotNone(review)

		# create a reply
		create_reply_url = reverse('movies.create_review_reply', args=[self.movie.id, review.id])
		response = self.client.post(create_reply_url, {'comment': 'Thanks!'})
		self.assertEqual(response.status_code, 302)

		reply = ReviewReply.objects.filter(review=review).first()
		self.assertIsNotNone(reply)
		self.assertEqual(reply.comment, 'Thanks!')

	def test_reply_shown_on_movie_page(self):
		self.client.login(username='tester', password='pass')
		self.client.post(reverse('movies.create_review', args=[self.movie.id]), {'comment': 'Great!'})
		review = Review.objects.filter(movie=self.movie).first()
		self.client.post(reverse('movies.create_review_reply', args=[self.movie.id, review.id]), {'comment': 'Thanks!'})

		response = self.client.get(reverse('movies.show', args=[self.movie.id]))
		self.assertContains(response, 'Thanks!')
