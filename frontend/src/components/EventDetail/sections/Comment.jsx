import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { LuTrash2 } from "react-icons/lu";
import { FiEdit2, FiMessageSquare } from "react-icons/fi";
import api from '../../../api';

export function CommentSection({ event }) {
  const [comments, setComments] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm();

  const end_point = {
    getEventComments: async (eventId) => {
      try {
        const response = await api.get(`/events/${eventId}/comments`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        return response.data;
      } catch (error) {
        throw new Error('Error fetching comments: ' + (error.response.data?.error));
      }
    },
  
    writeComment: async (content, eventId) => {
      try {
        const formData = new FormData();
        formData.append('content', content);
    
        const response = await api.post(`/comments/write-comment/${eventId}`, formData, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
    
        return response.data;
      } catch (error) {
        throw new Error('Error creating comment: ' + (error.response.data?.error));
      }
    },
  
    deleteComment: async (commentId) => {
      try {
        const response = await api.delete(`/comments/${commentId}/delete/`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
  
        return response.status === 204;
      } catch (error) {
        throw new Error('Error deleting comment: ' + (error.response?.data?.error));
      }
    },
  
    editComment: async (commentId, content) => {
      try {
        const formData = new FormData();
        formData.append('content', content);
  
        const response = await api.put(`/comments/${commentId}/edit/`, formData, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
  
        return response.data;
      } catch (error) {
        throw new Error('Error editing comment: ' + (error.response?.data?.error));
      }
    }
  };
  useEffect(() => {
    const fetchComments = async () => {
      if (!event?.id) return;
      
      try {
        setIsLoading(true);
        setError(null);
        const fetchedComments = await end_point.getEventComments(event.id);
        setComments(fetchedComments);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };
  
    fetchComments();
  }, [event?.id]);
  

  const onSubmit = async (data) => {
    if (!event?.id) return;
  
    try {
      setIsLoading(true);
      setError(null);
      
      const newComment = await end_point.writeComment(data.content, event.id);
      setComments(prev => [newComment, ...prev]);
      reset();
      
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (commentId) => {
    try {
      setIsLoading(true);
      setError(null);
      
      await end_point.deleteComment(commentId);
      setComments(prev => prev.filter(comment => comment.id !== commentId));
      
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="mb-8">
  <textarea
    {...register('content', { 
      required: 'Comment cannot be empty',
      maxLength: {
        value: 500,
        message: 'Comment is too long'
      }
    })}
    placeholder="Share your thoughts..."
    className="textarea textarea-bordered bg-white w-full mb-2"
    disabled={isLoading}
  />
  {errors.content && (
    <p className="text-sm text-red-500 mb-2">{errors.content.message}</p>
  )}
  <button 
    type="submit" 
    className="btn bg-amber-300"
    disabled={isLoading}
  >
    {isLoading ? 'Posting...' : 'Post Comment'}
  </button>
  <button
  className="btn btn-ghost btn-xs"
  onClick={() => handleDelete(comment.id)}
  disabled={isLoading}
>
  <LuTrash2 className="h-4 w-4" />
</button>
</form>
  )
}
