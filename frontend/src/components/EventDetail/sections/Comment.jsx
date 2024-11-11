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
  
  const handleEdit = async (commentId, newContent) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const updatedComment = await end_point.editComment(commentId, newContent);
      setComments(prev =>
        prev.map(comment =>
          comment.id === commentId ? updatedComment : comment
        )
      );
      setEditingId(null);
      
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (!event?.id) {
    return <div>No event selected</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <div className="card p-6 shadow-lg">
        <div className="flex items-center gap-2 mb-6">
          <FiMessageSquare className="h-5 w-5" />
          <h2 className="text-2xl font-semibold">Comments</h2>
        </div>

        {error && (
          <div className="alert alert-error mb-4">
            <p>{error}</p>
          </div>
        )}

        {/* Comment Form */}
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
            className="textarea textarea-bordered w-full mb-2"
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
        </form>

        {/* Comments List */}
        <div className="space-y-6">
          {comments.map(comment => (
            <div key={comment.id} className="flex gap-4">
              <div className="avatar w-10 h-10">
                <div className="rounded-full ring ring-amber-300 ring-offset-base-100 ring-offset-2">
                  <img src={comment.user.avatar} alt={comment.user.username} />
                </div>
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h3 className="font-medium text-black text-xl">{comment.user.username}</h3>
                  <div className="flex items-center gap-2">
                    <button
                      className="btn btn-ghost btn-xs"
                      onClick={() => setEditingId(comment.id)}
                      disabled={isLoading}
                    >
                      <FiEdit2 className="h-4 w-4" />
                    </button>
                    <button
                      className="btn btn-ghost btn-xs"
                      onClick={() => handleDelete(comment.id)}
                      disabled={isLoading}
                    >
                      <LuTrash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
                {editingId === comment.id ? (
                  <form
                    onSubmit={e => {
                      e.preventDefault();
                      const formData = new FormData(e.currentTarget);
                      handleEdit(comment.id, formData.get('content'));
                    }}
                    className="mt-2"
                  >
                    <textarea
                      name="content"
                      defaultValue={comment.content}
                      className="textarea textarea-bordered w-full mb-2"
                      disabled={isLoading}
                    />
                    <div className="flex gap-2">
                      <button 
                        type="submit" 
                        className="btn bg-amber-300 btn-xs"
                        disabled={isLoading}
                      >
                        {isLoading ? 'Saving...' : 'Save'}
                      </button>
                      <button
                        type="button"
                        className="btn btn-outline btn-xs"
                        onClick={() => setEditingId(null)}
                        disabled={isLoading}
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                ) : (
                  <p className="text-muted mt-1">{comment.content}</p>
                )}
                <span className="text-sm text-muted mt-1">
                  {new Date(comment.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}