import styles from "./index.module.css";
import api from "../../../../services/api";
import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { set } from "react-hook-form";

const mockPost: Post = {
    id: "1",
    author: "Jane Doe",
    title: "Introduction to TypeScript",
    content: "TypeScript extends JavaScript by adding types to the language. TypeScript speeds up your development experience by catching errors and providing fixes before you even run your code.",
    num_likes: 3,
    users_who_liked: ["user1", "user2", "user3"],
    num_comments: 2,
    comments: [
        {
            id: "c1",
            author: "John Doe",
            content: "Great article, very informative!"
        },
        {
            id: "c2",
            author: "Sarah Smith",
            content: "Thanks for sharing, learned a lot."
        }
    ],
    topic: "Programming",
    date: "2023-04-01T12:00:00Z"
};

interface Comment {
    id: string;
    author: string;
    content: string;
}
interface Post {
	id: string;
    author: string;
    title: string;
    content: string;
    num_likes: number;
    users_who_liked: string[];
    num_comments: number;
    comments: Comment[];
    topic: string;
    date: string;
}

const PostPage = () => {
	const navigate = useNavigate();
	const {post_id} = useParams<{
		post_id: string;
	}>();
	const [post, setPost] = useState<Post>(mockPost);
	const [comments, setComments] = useState<Comment[]>([]);
	const [likes, setLikes] = useState<string[]>([]);

	const loadPostDetails = async (post_id) => {
		try {
			const response = await api.get(
				`/forum/post/${post_id}`
			);

			const post = mockPost; //response.data;
			setPost(post);
			const comments = post.comments;
			setComments(comments);
			const likes = post.users_who_liked;
			setLikes(likes);
			
		} catch (error) {
			console.error(error);
		}
	};

	const handleDelete = async () => {
		try {
			await api.delete(`/forum/post/${post_id}`);
			alert("Post deletado com sucesso!");
			navigate(-1);
		} catch (error) {
			const axiosError = error as AxiosError;
			if (axiosError.response) {
			  alert(axiosError.response.statusText);
			} else {
			  alert(axiosError.message);
			}
		}
	};

	useEffect(() => {
		loadPostDetails(post_id);
	}, [likes, comments]);

	return (
		<div className={styles.pageContainer}>
			<h1>Post</h1>
			<div className={styles.container}>
				{post && (
				<div>
					<div className={styles.postTitle}>
						<h2>{post.title}</h2>
					</div>
					<div className={styles.author}>
						<p>Por {post.author}</p>
					</div>
					<div className={styles.contentContainer}>
						<p>{post.content}</p>
					</div>
					<div className={styles.postInfo}>
						<div className={styles.infoDisplay}>
							<p>{post.num_likes}&nbsp; </p>
							<Link 
								to={`/forum/post/${post.id}/likes`}
								style={{ textDecoration: "none", color: "#000"}}
							>
								
								Curtidas 
							</Link>
						</div>
						<div className={styles.infoDisplay}>
							<p>{post.num_comments} Comentários</p>
						</div>
					</div>
				</div>

				)}
				
				<div className={styles.commentSectionContainer}>
					{comments.map((comment, index) => (
						<div className={styles.commentContainer} key={index}>
							<Link
							to={{
								pathname: `/profile/${comment.author}`,
							}}
							style={{
								textDecoration: "none",
								color: "black",
								fontWeight: "bold",
							}}
							>
							<p>{comment.author}</p>
							</Link>
							<p>: {comment.content}</p>
						</div>
					))}
				</div>
			</div>
    	</div>
	);
};

export default PostPage;
